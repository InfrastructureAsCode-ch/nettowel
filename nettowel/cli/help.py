from io import StringIO
from qrcode import QRCode

HELP_MARKDOWN = """
**NetTowel** is a collection of network automation functions. 
> This project is in an early stage and still under heavy development.

Use cases
- Demonstrations
- Troubleshooting
- Fun

"""


def get_qrcode(data: str) -> str:
    qr = QRCode()
    qr.add_data(data)
    out = StringIO()
    qr.print_ascii(out)
    out.seek(0)
    return out.read()
