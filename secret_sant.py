# python -m smtpd -c DebuggingServer -n localhost:1025

from itertools import combinations, permutations
import pandas as pd
from random import shuffle, randint
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def generate():
    people_list = ['Make your own List']
    

    # comb = combinations(people_list, len(people_list)) 
    perm = permutations(people_list)

    def is_valid(order):
        # Add your constraints
        constraints = {
            "Name1": ["Name1"],
            "Name2": [],
            "Name3": [],
        }
        order_size = len(order)
        for i in range(len(order)):
            person = order[i]
            next_person = order[(i+1)%order_size]
            if next_person in constraints[person]:
                return False
        return True



    valid_perms = []
    perm = list(perm)
    for i in range(len(perm)): 
        order = perm[i]
        if is_valid(order):
            valid_perms.append(list(order))

    # print(list(perm))
    df = pd.DataFrame(list(valid_perms))

    # create a doc for all valid combinations
    df.to_csv("secret_santa.csv", index=False, header=False)
    # print(df)


def get_random_order(filename):
    orders = pd.read_csv(filename).to_numpy()
    shuffle(orders)
    i = randint(0, len(orders))
    return orders[i]


def write_order_to_files(order):
    order_size = 9
    for i in range(len(order)):
        person = order[i]
        next_person = order[(i+1)%order_size]
        filename = person + ".txt"
        f = open(filename, "w")
        f.write(next_person)
        f.close()


def send_emails(order_table):
        
    # gmail_user = 'sergeychirkunov1@gmail.com'
    # gmail_password = 'sever1998'

    # I used gmail
    smtp_server = "smtp.gmail.com"
    port = 465  # For starttls
    sender_email = "youremail@gmail.com"  # Enter your address
    receiver_email = "receiveremail@gmail.com"  # Enter receiver address

    password = 'yourpassword'

    people = {
        "Name": {"email": "name@gmail.com", "gendre": "He", "details": "loves ..."},
        "Name1": {"email": "name1@gmail.com", "gendre": "She", "details": "loves ..."},
    }

    # def get_person_details(name):
    #     person = people[name]
    #     return (name, person['email'], person['gendre'], person['details'])
    def construct_message(name):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'Secret Santa'

        
        fp = open('message.html', 'rb')
        html_msg = fp.read()
        html_msg = html_msg.decode('utf-8')
        # name = "Lera"
        person = people[name]
        personal_msg = "{}. {} {}.".format(name, person['gendre'], person['details'])
        
        html_msg = html_msg.replace("“ X - Loves …”", personal_msg)
        # print(html_msg)
        msgText = MIMEText(str(html_msg), 'html')
        fp.close()

        # This example assumes the image is in the current directory
        # replace photo name with your photo
        fp = open('PHOTO-2018-12-15-15-16-03.jpg', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')

        msg.attach(msgText)
        msg.attach(msgImage)

        return msg
    
    def get_email(name):
        return people[name]['email']


    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        # santa = "Lera"
        # receiver_email = get_email(santa)
        server.login(sender_email, password)
        
        for santa in order_table:
            # print("Santa's email:")
            # print(get_email(santa))
            receiver_email = get_email(santa)
            
            # print("Message for santa:")
            # print(order_table[santa], people[order_table[santa]]['details'])

            msg = construct_message(order_table[santa])
            server.sendmail(sender_email, receiver_email, msg.as_string())


def order_to_dic(order):
    send_receive_table = {}
    order_size = len(order)
    for i in range(len(order)):
        sender = order[i]
        receiver = order[(i+1)%order_size]
        send_receive_table[sender] = receiver
    return send_receive_table

def get_santa_and_receiver(santa):
    df = pd.read_csv('santas.csv', names=['Santa', 'Receiver'])
    # print(df)
    row = df.loc[df["Santa"] == santa]
    # print(row)
    receiver = row["Receiver"].values
    # print(santa, receiver[0])

    return santa, receiver[0]

if __name__ == "__main__":
    order = get_random_order("secret_santa.csv")
    # print(order)
    # print(order_to_dic(order))
    table = order_to_dic(order)
    df = pd.DataFrame([table]).T
    # print(df)
    df.to_csv('santas.csv', index = True, header = False)
    send_emails(table)


    # santa, receiver = get_santa_and_receiver("Lera")
    # print(santa, receiver)
    # print(df)
    # for name in table:
    #     print("Receiver email:")
    #     print(name)

    #     print("Message details")
    #     print(table[name])
    # write_order_to_files(order)