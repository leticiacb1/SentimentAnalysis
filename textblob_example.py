from textblob import TextBlob

text1 = "What a damn company. You guys are the worst, you can't meet the deadline."
text2 = "Hello everybody"
text3 = "I am so happy to be here"

blob1 = TextBlob(text1)
blob2 = TextBlob(text2)
blob3 = TextBlob(text3)

print(f"Polarity of text1: {blob1.polarity}")
print(f"Polarity of text2: {blob2.polarity}")
print(f"Polarity of text3: {blob3.polarity}")