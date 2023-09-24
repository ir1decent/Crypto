from Crypto.Util.Padding import pad

in_filename = "test1.doc.enc"
out_filename = "received_file.out"
with open(in_filename, "rb") as infile:
    filesize = int.from_bytes(infile.read(8), byteorder="big")
    iv = infile.read(16)
    with open(out_filename, "wb") as outfile:
        while True:
            chunk = infile.read(2048)
            print("hi")
            if len(chunk) == 0:
                break
            if len(chunk) % 16 != 0:
                chunk = pad(chunk, 16)
            outfile.write(chunk)
            # print("receive:",chunk.decode('utf-8','ignore'))
