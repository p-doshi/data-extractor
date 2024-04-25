import pandas as pd
import os
import nltk
import syllapy

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

positive_words = set(open("positive-words.txt").read().splitlines())
negative_words = set(open("negative-words.txt").read().splitlines())

extracted_folder = "C:/Users/Parth/pythonProject/output"
output_file = "C:/Users/Parth/pythonProject/black_coffer/Output_Data_Structure.xlsx"
output_data = []

for filename in os.listdir(extracted_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(extracted_folder, filename), "r", encoding="utf-8") as file:
            text = file.read()

        def positive_score(article_text):
            words = article_text.split()
            return sum(1 for word in words if word.lower() in positive_words)

        def negative_score(article_text):
            words = article_text.split()
            return sum(1 for word in words if word.lower() in negative_words)

        def polarity_score(score_pos, score_neg):
            return (score_pos - score_neg) / ((score_pos + score_neg) + 0.000001)

        def subjectivity_score(score_pos, score_neg, total_words):
            return (score_pos + score_neg) / (total_words + 0.000001)

        def avg_sentence_length(article_text):
            sentences = nltk.sent_tokenize(article_text)
            return sum(len(nltk.word_tokenize(sentence)) for sentence in sentences) / len(sentences)

        def percentage_complex_words(article_text):
            words = nltk.word_tokenize(article_text)
            tagged = nltk.pos_tag(words)
            comp_word_count = sum(1 for word, tag in tagged if tag.startswith('JJ') or tag.startswith('RB'))
            return (comp_word_count / len(words)) * 100

        def fog_index(average_sent_length, percent_complex_words):
            return 0.4 * (average_sent_length + percent_complex_words)

        def avg_words_per_sentence(article_text):
            words = nltk.word_tokenize(article_text)
            sentences = nltk.sent_tokenize(article_text)
            return len(words) / len(sentences)

        def syllable_count(word):
            return max(1, syllapy.count(word))

        def personal_pronouns(article_text):
            words = nltk.word_tokenize(article_text)
            tagged = nltk.pos_tag(words)
            return sum(1 for word, tag in tagged if tag == 'PRP')

        def avg_word_length(article_text):
            words = nltk.word_tokenize(article_text)
            return sum(len(word) for word in words) / len(words)

        pos_score = positive_score(text)
        neg_score = negative_score(text)
        polarity = polarity_score(pos_score, neg_score)
        subjectivity = subjectivity_score(pos_score, neg_score, len(nltk.word_tokenize(text)))
        avg_sent_length = avg_sentence_length(text)
        percent_complex = percentage_complex_words(text)
        fog = fog_index(avg_sent_length, percent_complex)
        avg_words_sent = avg_words_per_sentence(text)
        complex_word_count = sum(1 for word in nltk.word_tokenize(text) if syllable_count(word) > 2)
        word_count = len(nltk.word_tokenize(text))
        syllables_per_word = sum(syllable_count(word) for word in nltk.word_tokenize(text)) / max(1, word_count)
        personal_pronoun_count = personal_pronouns(text)
        avg_word_len = avg_word_length(text)

        output_data.append([
            filename.split(".")[0],  # URL_ID
            pos_score,
            neg_score,
            polarity,
            subjectivity,
            avg_sent_length,
            percent_complex,
            fog,
            avg_words_sent,
            complex_word_count,
            word_count,
            syllables_per_word,
            personal_pronoun_count,
            avg_word_len
        ])

df_output = pd.DataFrame(output_data, columns=[
    "URL_ID",
    "POSITIVE SCORE",
    "NEGATIVE SCORE",
    "POLARITY SCORE",
    "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH",
    "PERCENTAGE OF COMPLEX WORDS",
    "FOG INDEX",
    "AVG NUMBER OF WORDS PER SENTENCE",
    "COMPLEX WORD COUNT",
    "WORD COUNT",
    "SYLLABLE PER WORD",
    "PERSONAL PRONOUNS",
    "AVG WORD LENGTH"
])

df_output.to_excel(output_file, index=False)
print("Textual analysis completed and saved to Output Data Structure File")
