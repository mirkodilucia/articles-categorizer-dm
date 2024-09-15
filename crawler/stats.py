import json
import os
import matplotlib.pyplot as plt

from classifier.preprocessor import preprocess


def readAllFileInDirectory(directory):
    # Create a dictionary to store the top words in each directory
    word_count = {}

    # Loop through all the directories in the given directory
    with os.scandir(directory) as entries:
        for file in entries:
            with open(file, "r") as f:
                content = f.read()
                words = preprocess(content)

                for word in words:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

    print(word_count)
    return word_count


def readAllTopWordsInEachDirectory(directory):
    # Create a dictionary to store the top words in each directory
    categories = {}

    # Loop through all the directories in the given directory
    with os.scandir(directory) as entries:
        for entry in entries:

            if entry.is_dir():
                categories[entry.name] = {}

                # Create a dictionary to store the top words in the current directory
                word_count = readAllFileInDirectory(entry.path)

                # Sort the words by frequency
                sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

                # Store the top 10 words in the dictionary
                categories[entry.name] = sorted_words[:10]

    # Save the top words in each directory to a file
    with open("top_words.json", "w") as f:
        json.dump(categories, f)

    print(categories)


def count_files_in_directory(directory):
    file_counts = {}
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            file_count = sum([len(files) for r, d, files in os.walk(dir_path)])
            file_counts[dir_name] = file_count
    return file_counts


def plot_file_counts(file_counts):
    print(file_counts)
    print("total", sum(file_counts.values()))
    plt.figure(figsize=(10, 5))
    plt.xlabel('Categories')
    plt.ylabel('Number of Articles')
    plt.title('Number of articles for each category')

    # change colors of each bar
    colors = ['purple', 'teal', 'brown', 'pink', 'orange', 'olive', 'lime', 'blue', 'red', 'green', 'yellow', 'gray']
    for i, key in enumerate(file_counts.keys()):
        plt.bar(key, file_counts[key], color=colors[i])

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


def readTopWordsAndPrintForSlide(file):
    with open(file, "r") as f:
        data = json.load(f)

        result = ""
        # Create a string with - Category: (word, frequency) - format
        for category in data:
            result += f"- {category}: "
            for word in data[category]:
                result += f"({word[0]}, {word[1]}), "

            result += "\n"

        print(result)
    return result


if __name__ == '__main__':
    readAllTopWordsInEachDirectory("./data")
    readTopWordsAndPrintForSlide("top_words.json")

    total_articles_directory = 'classifier/data/articles'
    file_counts = count_files_in_directory(total_articles_directory)
    plot_file_counts(file_counts)

    trained_articl_data = 'classifier/data/dataset/train'
    file_counts = count_files_in_directory(trained_articl_data)
    plot_file_counts(file_counts)

    test_articl_data = 'classifier/data/dataset/tests'
    file_counts = count_files_in_directory(test_articl_data)
    plot_file_counts(file_counts)
