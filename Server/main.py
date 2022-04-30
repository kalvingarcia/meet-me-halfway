# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor
import os
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import mysql.connector

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


# Class to handle the data sent from connection. Each instance is connection
class MITMServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


# Factory class to initialize new connections as MITMServer classes
class MITMServerFactory(protocol.Factory):
    protocol = MITMServer

    def __init__(self, app):
        self.app = app


# App that runs it all
class MITMServerApp(App):
    label = None
    textbox = None

    #Connecting to db. Cursor is used to query the db. connection is for commiting a edit to the db
    def database_auth():
            try:
                connection = mysql.connector.connect(
                    user='doadmin',
                    password ='AVNS_WZEScW_Y5FNKr7m',
                    host='db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com',
                    port = 25060,
                    database='defaultdb'
                )
                print('\n[+] Connected to db-mysql-teamrocket-do-user-11106141-0.b.db.ondigitalocean.com Successfully')

                cursor = connection.cursor()

                return cursor, connection
            except BaseException as e:
                print(str(e))
    # Databse Connection vars. connectionarray holds variables to query and modify db

    connectorarr = database_auth()
    cursor = connectorarr[0]
    connection = connectorarr[1]

    # Initializing the server
    def build(self):
        root = self.setup_gui()
        self.listen_for_client()
        return root

    # Setting up the gui
    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    # Waiting for client connection
    def listen_for_client(self):
        reactor.listenTCP(25565, MITMServerFactory(self))

    # Taking input from console line and processing it locally on server
    def send_message(self, *args):
        msg = self.textbox.text
        if msg:
            self.print_message(f"{msg}")
            self.textbox.text = ""
            return (msg.encode('utf-8'))

    # Handling the messages sent by the client
    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.print_message("\nreceived:  {}\n".format(msg))
        msg = json.loads(msg)
        response = "failure"

        # Checking for keywords from input
        if msg['command'] == "login":
            self.print_message("Starting Login Process")
            response = self.auth_login(msg)
            self.print_message(f"Response: {response['result']}")

        # Checking for registration
        if msg['command'] == "register":
            self.print_message("Starting Registration Process")
            response = self.auth_regi(msg)

        # Checking for Creation of new meeting
        if msg['command'] == 'create_meeting':
            self.print_message("Starting New Meeting")

        self.label.text += "responded: {}\n".format(response)
        return (json.dumps(response).encode('utf-8'))

    # Print message to console on server
    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)

    # Defining the authentication function
    def auth_login(self, msg):
        # Setting up json message to send back
        response = {'command': 'auth_login'}

        self.cursor.execute("Select * From User where Username = '{}' and Password = '{}' ".format(msg['username'],msg['password']))
        result = self.cursor.fetchall()
        if(result == []):
            response['result'] = "fail"
        else:
            response['result'] = "success"
        return response

    # Defining the registration function
    def auth_regi(self, msg):
        response = {'command': 'auth_register'}
        #TODO change * to username
        self.cursor.execute("Select * From User where Username = '{}'".format(msg['username']))
        result = self.cursor.fetchall()
        self.print_message(result)
        if(result != []):
            response['result'] = "username_exists"
            self.print_message(response)
            return response

        self.cursor.execute("Select * From User where Email = '{}' ".format(msg['email']))
        result = self.cursor.fetchall()
        if(result != []):
            response['result'] = "email_exists"
            self.print_message(response)
            return response


        sql = 'INSERT INTO User (Name, Email, Password, Username) VALUES (%s,%s,%s,%s)'
        val = (msg['name'], msg['email'], msg['password'], msg['username'])
        self.cursor.execute(sql,val)
        self.connection.commit()
        
        response['result'] = "success"
        return response

    # Defining the new meeting creation function
    def new_meeting(self, msg):
        # Make new table entry in database
        # add user information from given login
        # Find other user and send invite by adding it to table in database
            # This may require on login/ random refresh for users to check for any invites.
        # Here is what we want passed to server
            # datetime
            # Locations filters
            # User invited
            # user ID (for location finding in DB)
        self.print_message("Inside new_meeting Function")



if __name__ == '__main__':
    MITMServerApp().run()
