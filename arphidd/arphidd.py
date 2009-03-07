from smartcard.System import readers

def get_direct_tx(command):
	return [0xFF, 0x00, 0x00, 0x00] + [len(command)] + command

def get_response(length):
	return [0xFF, 0xC0, 0x00, 0x00] + [length]

def get_led_control(led_state, control):
	return [0xFF, 0x00, 0x40] + [led_state] + [0x04] + control


def get_set_retry_time_to_one():
	return get_direct_tx([0xD4, 0x32, 0x05, 0x00, 0x00, 0x00])

class Poller():
	def __init__(self):
		r = readers()
		self.ttag = r[r.index('ACS ACR 38U-CCID 00 00')].createConnection()
		self.ttag.connect()
		#set retry time to 1
		RTO = get_set_retry_time_to_one()
		data, sw1, sw2 = self.ttag.transmit( RTO )

	def poll(self):
		POLL = [0xD4, 0x4A, 0x01, 0x00]
		data, sw1, sw2 = self.ttag.transmit( get_direct_tx(POLL) )
		if sw1 == 0x61:
			data, sw1, sw2 = self.ttag.transmit( get_response(sw2) )
			if data[2] == 0: #no tag found	
				#flash led and poll again
				print "no tag"
				self.ttag.transmit(get_led_control(0x50, [0x05, 0x05, 0x03, 0x01]))
				self.poll()
			else:
				print data
				self.poll()

poller = Poller()
poller.poll()
