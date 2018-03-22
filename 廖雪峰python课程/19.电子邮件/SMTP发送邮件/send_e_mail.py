from_addr = check_e_mail_v2(raw_input('From: '))
password = raw_input('Password: ')
smtp_server = raw_input('SMTP server: ')
smtp_port = int(raw_input('Port of SMTP server: '))
to_addr = check_e_mail_v2(raw_input('To: '))
msg = raw_input('Message: ')
import smtplib
server = smtplib.SMTP(smtp_server,smtp_port)#Default port 25
server.starttls()
server.set_debuglevel(1)
server.login(from_addr.address,password)
server.sendmail(from_addr.address,[to_addr.address],msg.as_string())
server.quit()