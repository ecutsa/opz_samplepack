import wave, os, glob, audiosegment, binascii, re, sys, struct, fnmatch

#FORM
riff = '464f524d'
file_size = '00037f14'
aiff = '41494646'
form = riff+file_size+aiff
#COMM
comm = '434f4d4d0000001200010001b21e0010400eac44'
appchunk='0000000000004150504c000005b4'
forge_1='6f702d317b20226472756d5f76657273696f6e22203a20332c202264796e615f656e7622203a205b20302c20383139322c20302c20302c20302c20302c20302c2030205d2c20226564697461626c6522203a20747275652c2022656e6422203a20205b20'
forge_end='32383836343432302c2035373732383834302c2038363539333236302c203131353435373638302c203134343332363135392c203137333139303537392c203230323035343939392c203233303932333437372c203235393738373839382c203238383635323331382c203331373532303739362c203334363338353231362c203337353234393633362c203430343131383131352c203433323938323533352c203436313834363935352c2035373732383834302c203131353435373638302c203137333139303537392c203233303931393431392c203238383635323331382c203334363338353231362c203430343131343035372c20343631383436393535'
forge_2='205d2c202266785f61637469766522203a2066616c73652c202266785f706172616d7322203a205b20383030302c20383030302c20383030302c20383030302c20383030302c20383030302c20383030302c2038303030205d2c202266785f7479706522203a202264656c6179222c20226c666f5f61637469766522203a2066616c73652c20226c666f5f706172616d7322203a205b20302c20302c20302c20302c20302c20302c20302c2030205d2c20226c666f5f7479706522203a20227472656d6f6c6f222c20226e616d6522203a202275736572222c20226f637461766522203a20302c2022706974636822203a205b20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c20302c2030205d2c2022706c61796d6f646522203a20205b2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c2031363338342c203136333834205d2c20227265766572736522203a20205b20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c2038313932205d2c2022737461727422203a20205b20'
forge_start ='302c2032383836343432302c2035373732383834302c2038363539333236302c203131353436313733382c203134343332363135392c203137333139303537392c203230323035393035372c203233303932333437372c203235393738373839382c203238383635363337362c203331373532303739362c203334363338353231362c203337353235333639342c203430343131383131352c203433323938323533352c20302c2035373732383834302c203131353436313733382c203137333139303537392c203233303932333437372c203238383635363337362c203334363338353231362c20343034313138313135'
forge_3 ='205d2c20227479706522203a20226472756d222c2022766f6c756d6522203a20205b20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c20383139322c2038313932205d207d20'
ssnd='53534e44000379320000000000000000'

cwd = os.path.split(os.getcwd())
path = '.'
nb_sample=0
nb_pack=1
current_sample=0
silence_duration = 50 # silence between samples in milliseconds
silence = audiosegment.silent(silence_duration).resample(sample_rate_Hz=44100, sample_width=2, channels=1)
ratio= 178966 #ratio for drumv3
start = [0] * 24 # create an array of 24 elements for the starts points
end = [1] * 24 # create an array of 24 elements for the ends points
current_seg = []
seg_final = []

def init_pack():
    start = [0] *24
    end = [1] * 24
    current_seg = []
    seg_final = []

def create_directory(filenumber):
    try:
        os.rmdir("./0"+filenumber)
    except OSError:
        pass
    try:
        os.makedirs("./"+filenumber)
    except OSError:
        pass

def format_array(array):
    array = [x * ratio for x in array]
    array = [ round(elem) for elem in array ]
    array = str.encode(str(array).strip('[]'))
    array = binascii.hexlify(array).decode('utf-8')
    return array
def set_parity(forge_hex):
    forge_ascii = binascii.unhexlify(forge_hex.encode('utf-8'))
    forge_ascii = sys.getsizeof(forge_ascii)-41+8
    if forge_ascii % 2 == 0:
        pass # Even
    else:
        forge_hex = forge_hex+'00'
        pass # Odd
    return forge_hex

def create_pack(start, end, filenumber):
    outfile='./'+filenumber+'/'+cwd[1]+filenumber+'.aif'
    create_directory(filenumber)
    start = format_array(start)
    end = format_array(end)
    seg_final.export(outfile, format="aiff", parameters=["-c:a", "pcm_s16be"])
    filesize = os.path.getsize(outfile)
    with open(outfile, 'rb') as f:
        content = f.read()
        ascii = binascii.hexlify(content).decode('utf-8')
        forged_op1_hex = forge_1+end+forge_2+start+forge_3
        forged_op1_hex = set_parity(forged_op1_hex)
        header = form+comm+appchunk+forged_op1_hex+ssnd
        written_comm = re.search(r"(?<=434f4d4d000000120001).{8}", ascii) #GET COM SAMPLE RATE
        written_ssnd = re.search(r"(?<=53534e44)(.{8})", ascii)
        ascii = re.sub(r".*(?<=53534e44)(.{24})", header, ascii, count=1)
        ##########################################
        #SET OP1 SIZE
        forged_op1_ascii = binascii.unhexlify(forged_op1_hex.encode('utf-8'))
        forged_op1_ascii = sys.getsizeof(forged_op1_ascii)-41+8
        forged_op1_ascii = binascii.hexlify((forged_op1_ascii).to_bytes(4, byteorder='big')).decode('utf-8')
        ascii = re.sub(r"(?<=4150504c)(.{8})", forged_op1_ascii, ascii, count=1)
        #SSND
        written_ssnd = written_ssnd.group(0)
        ascii = re.sub(r"(?<=53534e44)(.{8})", written_ssnd, ascii, count=1) #regex SSND
        #COMM
        written_comm = written_comm.group(0)
        ascii = re.sub(r"(?<=434f4d4d000000120001).{8}", written_comm, ascii, count=1)
        #SET DATASIZE AIFF
        content = binascii.unhexlify(ascii.encode('utf-8'))
        written_form = sys.getsizeof(content)-42
        written_form = binascii.hexlify((written_form).to_bytes(4, byteorder='big')).decode('utf-8')
        ascii = re.sub(r"(?<=464f524d)(.*)(?=41494646)", written_form, ascii, count=1) #FORM

        content = binascii.unhexlify(ascii.encode('utf-8'))
        os.remove(outfile)
        file = open(outfile,"xb")
        file.write(content)
        file.close()
        print(outfile, " has been created.")

tot_samples=len(fnmatch.filter(os.listdir(path), '*.wav'))

for filename in glob.glob(os.path.join(path, '*.wav')):
    lenght_seg=len(seg_final)
    start[nb_sample]= lenght_seg
    if nb_sample == 0:
        seg_final= audiosegment.from_file(filename).resample(sample_rate_Hz=44100, sample_width=2, channels=1)
    else:
        seg_final+= audiosegment.from_file(filename).resample(sample_rate_Hz=44100, sample_width=2, channels=1)
    lenght_seg=len(seg_final)
    if lenght_seg > 12000:
        print("This sample pack is longer than 12 seconds and will not work")
        pass
    end[nb_sample]=lenght_seg
    nb_sample += 1
    current_sample += 1
    if (current_sample % 24 == 0) | ((tot_samples-current_sample) == 0):
        filenumber='0'+str(nb_pack)
        create_pack(start, end, filenumber)
        nb_pack += 1
        nb_sample = 0
        init_pack()
