plain_file = open("D:\\python\\final\\test\\plain.txt", "r")
plain_text = plain_file.read()
decrypted_file = open("D:\\python\\final\\test\\decrypted.txt", "r")
decrypted_text = decrypted_file.read()
result = plain_text == decrypted_text

assert(result)
print(result)
