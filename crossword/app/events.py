'''
Created on Mar 25, 2012

@author: alex
'''

from django_socketio import events
import sys

@events.on_connect
def connectHandler(request, socket, context):
    print "connect"
    print
    #socket.send("connect")
    
@events.on_message(channel="^xword$")
def messageHandler(request, socket, context, message):
    print "message"
    #socket.send("message")
    socket.broadcast_channel(message)
    #print "message"
    #print message
    
@events.on_subscribe(channel="^xword$")
def subscribe(request, socket, context, channel):
    print "subscribed to " + channel
    
