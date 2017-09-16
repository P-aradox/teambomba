text = "ECPTWNTTGFMGHIKGWWCNJPWRJUIJVVDQRNDPOUIVYHVWQKCHPTHLJKWXCZOCKHIGZOMIYCVHRSNZDTDUIFCRVWQKRLTOWHVNYPIIHVGMJNHV".upper()#open("ciphertext.txt", "r").read()
totalSum = 0
for chrIndex in range(65, 91):
    count = 0
    letter = chr(chrIndex)
    for c in text:
        if c == letter:
            count += 1
    if count != 0:
        totalSum += (count * (count - 1))
ioc = totalSum / (len(text) * (len(text) - 1))
print(ioc)
#English = 0.0667
