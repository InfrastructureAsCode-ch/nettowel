try:
    from ttp import ttp

    TTP_INSTALLED = True

except ImportError:
    TTP_INSTALLED = False

NOT_INSTALLED = "TTP is not installed. Install it with pip: pip install nettowel[ttp]"
