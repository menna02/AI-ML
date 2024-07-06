import qrcode
import qrcode.constants


def qr_code_maker(data, name):

    qr = qrcode.QRCode(version=1, 
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(name+'_qr.png')

data = 'https://github.com/menna02/AI-ML'
name = 'github_repo'
qr_code_maker(data, name)