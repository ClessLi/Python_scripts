from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import check_e_mail_v2
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))
def _format_title(s):
    return (Header(s, 'utf-8').encode() if isinstance(s, unicode) else s)


if __name__ == '__main__':
    from_addr = check_e_mail_v2.e_mail(raw_input('From: '))
    password = raw_input('Password: ')
    smtp_servoer = raw_input('SMTP server: ')
    print 'smtp-mail.outlook.com 587 STARTTLS'
    smtp_port = int(raw_input('Port of SMTP server: '))
    to_addr = check_e_mail_v2.e_mail(raw_input('To: '))
    title = raw_input('Title: ')
    msg = raw_input('Message: ')
    msg = MIMEText(msg,'plain','utf-8')
    msg['From'] = _format_addr(u'%s <%s>' % (from_addr.name,from_addr.address))
    msg['To'] = _format_addr(u'%s <%s>' % (to_addr.name,to_addr.address))
    msg['Subject'] = _format_title(title)
    #msg['Subject'] = Header(u'%s' % title,'utf-8').encode()
    server = smtplib.SMTP(smtp_server,smtp_port)#Default port 25
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr.address,password)
    server.sendmail(from_addr.address,[to_addr.address],msg.as_string())
    server.quit()
