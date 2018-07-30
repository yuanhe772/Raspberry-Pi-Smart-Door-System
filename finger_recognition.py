import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint


def finger(flag):

    # initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

    # gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    # search the finger and calculate hash
    try:
        while True:
            print('Waiting for finger...')

            # wait for that finger is read
            while ( f.readImage() == False ):
                pass

            # converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

            # searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found, please try again')
                return "Please retry.", positionNumber
            #exit(0)
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))

                # loads the found template to charbuffer 1
                f.loadTemplate(positionNumber, 0x01)

                # downloads the characteristics of template loaded in charbuffer 1
                characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

                # hashes characteristics of template
                print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
                #exit(0)
                
                if flag == 1:
                    if positionNumber == 0 or positionNumber == 1:
                        return "CONGRATULATIONS!", positionNumber
                    else:
                        return "Please retry.", positionNumber
                elif flag == -1:
                    if positionNumber == 2:
                        return "CONGRATULATIONS!", positionNumber
                    else:
                        return "Please retry.", positionNumber
                
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)