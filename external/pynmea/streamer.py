""" For dealing with streams of nmea data
"""
from pynmea.exceptions import NoDataGivenError


class NMEAStream(object):
    """ NMEAStream object is used to
    """
    def __init__(self, stream_obj=None):
        """ stream_obj should be a file like object.
            If the requirement is just to split data in memory, no stream_obj
            is required. Simply create an instance of this class and
            call _split directly with the data.
        """
        self.stream = stream_obj
        self.head = ''

    def get_strings(self, data=None, size=1024):
        """ Read and return sentences as strings
        """
        return self._read(data=data, size=size)

    def get_objects(self, data=None, size=1024):
        """ Get sentences but return list of NMEA objects
        """
        str_data = self._read(data=data, size=size)
        nmea_objects = []
        for nmea_str in str_data:
            try:
                nmea_ob = self._get_type(nmea_str)()
            except TypeError:
                # NMEA sentence was not recognised
                continue
            nmea_ob.parse(nmea_str)
            nmea_objects.append(nmea_ob)

        return nmea_objects


    def _read(self, data=None, size=1024):
        """ Read size bytes of data. Always strip off the last record and
            append to the start of the data stream on the next call.
            This ensures that only full sentences are returned.
        """
        if not data and not self.stream and not self.head:
            # If there's no data and no stream, raise an error
            raise NoDataGivenError('No data was provided')

        if not data and self.stream:
            read_data = self.stream.read(size)
        else:
            read_data = data

        data = self.head + read_data
        raw_sentences = self._split(data)
        if not read_data:
            self.head = ''
            return raw_sentences
        self.head = raw_sentences[-1]
        full_sentences = raw_sentences[:-1]
        return full_sentences

    def _get_type(self, sentence):
        """ Get the NMEA type and return the appropriate object. Returns
            None if no such object was found.

            TODO: raise error instead of None. Failing silently is a Bad Thing.
            We can always catch the error later if the user wishes to supress
            errors.
        """
        sen_type = sentence.split(',')[0].lstrip('$')
        sen_mod = __import__('pynmea.nmea', fromlist=[sen_type])
        sen_obj = getattr(sen_mod, sen_type, None)
        return sen_obj

    def _split(self, data, separator=None):
        """ Take some data and split up based on the notion that a sentence
            looks something like:
            $x,y,z or $x,y,z*ab

            separator is for cases where there is something strange or
            non-standard as a separator between sentences.
            Without this, there is no real way to tell whether:
            $x,y,zSTUFF
            is legal or if STUFF should be stripped.
        """
        sentences = data.split('$')
        clean_sentences = []
        for item in sentences:
            cleaned_item = item.rstrip()
            if separator:
                cleaned_item = cleaned_item.rstrip(separator)
            if '*' in cleaned_item.split(',')[-1]:
                # There must be a checksum. Remove any trailing fluff:
                try:
                    first, checksum = cleaned_item.split('*')
                except ValueError:
                    # Some GPS data recorders have been shown to output
                    # run-together sentences (no leading $).
                    # In this case, ignore error and continue, discarding the
                    # erroneous data.
                    # TODO: try and fix the data.
                    continue
                cleaned_item = '*'.join([first, checksum[:2]])
            if cleaned_item:
                clean_sentences.append(cleaned_item)

        return clean_sentences
