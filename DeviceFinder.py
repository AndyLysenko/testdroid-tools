# -*- coding: utf-8 -*-

import requests, sys

class DeviceFinder:
    # Cloud URL (not including API path)
    url = None

    """ Full constructor with username and password
    """
    def __init__(self, url="https://cloud.testdroid.com", download_buffer_size=65536):
        self.cloud_url = url
        self.download_buffer_size = download_buffer_size

    """ Append dictionary items to header
    """
    def _build_headers(self, headers=None):
        hdrs = {}
        hdrs["Accept"] = "application/json"
        if headers != None:
            hdrs.update(headers)
        return hdrs

    """ Returns list of devices
    """
    def get_devices(self, limit=0, search_string=""):
        if search_string:
            return self.get("devices?limit=%s&search=%s" % (limit, search_string))
        else:
            return self.get("devices?limit=%s" % (limit))

    """ GET from API resource
    """
    def get(self, path=None, get_headers=None):
        url = "%s/api/v2/%s" % (self.cloud_url, path)
        headers=self._build_headers(get_headers)
        res = requests.get(url, headers=self._build_headers(get_headers))
        if res.ok:
            return res.json()
        else:
            print "Could not retrieve free devices."
            sys.exit -1

    """ Find available free Android device
    """
    def available_free_android_device(self, limit=0):
        print "Searching Available Free Android Device..."

        for device in self.get_devices(limit)['data']:
            if device['creditsPrice'] == 0 and device['locked'] == False and device['osType'] == "ANDROID" and device['softwareVersion']['apiLevel'] > 16:
                print "Found device '%s'" % device['displayName']
                print ""
                print device
                return str(device['displayName'])

        print "No available device found"
        print ""
        return ""

    """ Check if device is available to use
    """
    def device_available(self, device_name, limit=0):
        print "Checking if device '%s' is available..." % device_name

        for device in self.get_devices(limit, device_name)['data']:
            print "Credit Price= %s" % device['creditsPrice']
            print "Is locked= %s" % device['locked']
            # print device     # prints full device data
            return not bool(device['locked'])
        else:
            print "Device with entered name was not found"
            return False


    """ Find available free iOS device
    """
    def available_free_ios_device(self, limit=0):
        print "Searching Available Free iOS Device..."

        for device in self.get_devices(limit)['data']:
            if device['creditsPrice'] == 0 and device['locked'] == False and device['osType'] == "IOS":
                print "Found device '%s'" % device['displayName']
                print ""
                return str(device['displayName'])

        print "No available device found"
        print ""
        return ""
    """ Find out the API level of a Device
    """
    def device_API_level(self, deviceName):
        print "Searching for API level of device '%s'" % deviceName

        try:
            device = self.get(path="devices?search=%s" % deviceName)
            apiLevel = device['data'][0]['softwareVersion']['apiLevel']
            print "Found API level: %s" % apiLevel
            return apiLevel
        except Exception, e:
            print "Error: %s" % e
            return
