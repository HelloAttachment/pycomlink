import unittest

import pycomlink as pycml

def load_and_clean_example_data():
    cml = pycml.io.examples.read_one_cml()
    cml.process.quality_control.set_to_nan_if('tx', '>=', 100)
    cml.process.quality_control.set_to_nan_if('rx', '==', -99.9)
    for cml_ch in cml.channels.values():
        cml_ch.data.interpolate(limit=3)
    return cml


class TestWetDryStdDev(unittest.TestCase):
    def test_standrad_processing(self):
        cml = load_and_clean_example_data()
        cml.process.wet_dry.std_dev(window_length=60, threshold=0.8)

        assert (cml.channel_1.data.wet.loc['2016-11-02 14:00'].values[0]
                == True)
        assert (cml.channel_1.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)

        assert (cml.channel_2.data.wet.loc['2016-11-02 14:00'].values[0]
                == True)
        assert (cml.channel_2.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)

        cml.process.wet_dry.std_dev(window_length=30, threshold=0.8)

        assert (cml.channel_1.data.wet.loc['2016-11-02 14:00'].values[0]
                == False)
        assert (cml.channel_1.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)
        assert (cml.channel_1.data.wet.loc['2016-11-02 14:30'].values[0]
                == True)

        assert (cml.channel_2.data.wet.loc['2016-11-02 14:00'].values[0]
                == False)
        assert (cml.channel_2.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)
        assert (cml.channel_2.data.wet.loc['2016-11-02 14:30'].values[0]
                == True)

    def test_processing_for_selected_time_period(self):
        cml = load_and_clean_example_data()

        # First as a comparisson the standard way
        cml.process.wet_dry.std_dev(window_length=60, threshold=0.8)

        assert (cml.channel_1.data.wet.loc['2016-11-02 18:30'].values[0]
                == True)
        assert (cml.channel_1.data.wet.loc['2016-11-02 14:00'].values[0]
                == True)
        assert (cml.channel_1.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)

        # Then for a period from a starting point in time
        t_start = '2016-11-02 14:30'
        cml.channel_1.data.wet = False
        cml.process.wet_dry.std_dev(window_length=60,
                                    threshold=0.8,
                                    t_start=t_start)
        assert (cml.channel_1.data.wet.loc['2016-11-02 18:30'].values[0]
                == True)
        assert (cml.channel_1.data.wet.loc['2016-11-02 14:00'].values[0]
                == False)
        assert (cml.channel_1.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)

        # Then for a period to a end point in time
        t_stop = '2016-11-02 15:00'
        cml.channel_1.data.wet = False
        cml.process.wet_dry.std_dev(window_length=60,
                                    threshold=0.8,
                                    t_stop=t_stop)
        assert (cml.channel_1.data.wet.loc['2016-11-02 18:30'].values[0]
                == False)
        assert (cml.channel_1.data.wet.loc['2016-11-02 14:00'].values[0]
                == True)
        assert (cml.channel_1.data.wet.loc['2016-11-02 13:00'].values[0]
                == False)