import hashlib,re
from datetime import datetime,timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
SOURCE_URL='https://www.basquetcatala.cat/partits/calendari_equip_global/129/89394'
OUTPUT=Path('basquet-alella-a.ics'); TZID='Europe/Madrid'
def esc(v): return v.replace('\\','\\\\').replace(';',r'\;').replace(',',r'\,').replace('\n',r'\n')
def main():
 r=requests.get(SOURCE_URL,timeout=30,headers={'User-Agent':'Mozilla/5.0 (compatible; BasquetAlellaCalendar/1.0)'}); r.raise_for_status()
 s=BeautifulSoup(r.text,'html.parser'); table=s.select_one('#tbl-clubs-list')
 if not table: raise RuntimeError('No se encontró la tabla #tbl-clubs-list en FCBQ.')
 matches=[]
 for tr in table.select('tbody tr'):
  tds=tr.find_all('td')
  if len(tds)<6: continue
  vals=[td.get_text(' ',strip=True) for td in tds[:6]]; date_s,time_s,home,away,category,venue=vals
  try: d=datetime.strptime(date_s,'%d/%m/%Y').date(); t=datetime.strptime(time_s,'%H:%M').time()
  except ValueError: continue
  mid=''
  for a in tr.find_all('a',href=True):
   m=re.search(r'/llistatpartits/(\d+)',a['href'])
   if m: mid=m.group(1); break
  matches.append({'date':d,'time':t,'home':home,'away':away,'category':category,'venue':venue,'id':mid})
 if len(matches)<20: raise RuntimeError(f'Solo se encontraron {len(matches)} partidos. Se cancela la actualización.')
 matches.sort(key=lambda x:(x['date'],x['time'],x['home'],x['away']))
 now=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
 lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Basquet Alella A//Calendario FCBQ//ES','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Basquet Alella A','X-WR-TIMEZONE:Europe/Madrid']
 for m in matches:
  start=datetime.combine(m['date'],m['time']); end=start+timedelta(hours=2)
  uidbase=m['id'] or hashlib.sha1(f"{m['date']}|{m['time']}|{m['home']}|{m['away']}".encode()).hexdigest()
  lines += ['BEGIN:VEVENT',f'UID:fcbq-{uidbase}@basquet-alella-calendar',f'DTSTAMP:{now}',f'DTSTART;TZID={TZID}:{start:%Y%m%dT%H%M%S}',f'DTEND;TZID={TZID}:{end:%Y%m%dT%H%M%S}',f"SUMMARY:{esc(m['home']+' vs '+m['away'])}",f"LOCATION:{esc(m['venue'])}",f"DESCRIPTION:{esc(m['category']+chr(10)+m['venue'])}",'END:VEVENT']
 lines.append('END:VCALENDAR'); OUTPUT.write_text('\r\n'.join(lines)+'\r\n',encoding='utf-8'); print(f'Calendario actualizado: {len(matches)} partidos')
if __name__=='__main__': main()
