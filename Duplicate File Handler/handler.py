import operator
import os
import sys
import hashlib


class Application:
    def __init__(self, path):
        self.wrong = "Wrong option\n"
        self.files = list()
        for root, _, file in os.walk(path, topdown=True):
            for name in file:
                temp = os.path.join(root, name)
                self.files.append({'path': temp, 'extension': os.path.splitext(temp)[1],
                                   'size': os.path.getsize(temp), 'hash': self.__get_file_hash(temp)})

    def __get_file_hash(self, file_name):
        with open(file_name, mode='rb') as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def run(self):
        print("Enter file format:")
        file_extension = f".{input()}"
        print("""
Size sorting options:
1. Descending
2. Ascending\n""")
        sort_order = int(self.__choice_order())
        duplicates = self.__find_duplicates_by_size(file_extension, sort_order)

        while True:
            print("Check for duplicates?")
            if input().lower() == "yes":
                print()
                break
            else:
                print(self.wrong)

        duplicates = self.__find_duplicates_by_hash(duplicates, sort_order)

        print("Delete files?")
        indexes = self.__input_file_indexes_for_delete(duplicates)
        self.__delete_files(indexes, duplicates)

    def __choice_order(self):
        while True:
            print("Enter a sorting option:")
            try:
                order = int(input())
                if 3 > order > 0:
                    return order
                else:
                    print(self.wrong)
            except ValueError:
                print(self.wrong)

    def __find_duplicates_by_size(self, file_extension, order):
        duplicates = dict()
        for f in self.files:
            if len(file_extension) == 1 or f['extension'] == file_extension:
                if not duplicates.keys().__contains__(f['size']):
                    duplicates[f['size']] \
                        = [{'path': f['path'], 'extension': f['extension'], 'hash': f['hash'], 'size': f['size']}]
                else:
                    duplicates[f['size']] \
                        .append({'path': f['path'], 'extension': f['extension'], 'hash': f['hash'], 'size': f['size']})

        for size, files in sorted(duplicates.items(), key=operator.itemgetter(0),
                                  reverse=True if order == 1 else False):
            print(f"{size} bytes")
            for f in files:
                print(f['path'])
            print()
        return duplicates

    def __find_duplicates_by_hash(self, duplicates_by_size, order):
        number_of_file = 1
        duplicates = dict()
        for size, files_by_size in sorted(duplicates_by_size.items(), key=operator.itemgetter(0),
                                          reverse=True if order == 1 else False):
            print(f"{size} bytes")
            duplicates_by_hash = dict()
            for f in files_by_size:
                if not duplicates_by_hash.keys().__contains__(f['hash']):
                    duplicates_by_hash[f['hash']] = [{'path': f['path'], 'size': f['size']}]
                else:
                    duplicates_by_hash[f['hash']].append({'path': f['path'], 'size': f['size']})

            for h, files_by_hash in duplicates_by_hash.items():
                if len(files_by_hash) > 1:
                    print(f"Hash: {h}")
                    for f in files_by_hash:
                        print(f"{number_of_file}. {f['path']}")
                        duplicates[number_of_file] = f
                        number_of_file += 1
            print()
        print()
        return duplicates

    def __input_file_indexes_for_delete(self, duplicates):
        while True:
            if input('\n').lower() == "yes":
                print("Enter file numbers to delete:")
                indexes = list()
                is_valid_indexes = True
                for i in input().split(" "):
                    if not i.isdigit():
                        print(self.wrong)
                        is_valid_indexes = False
                        break
                    if not duplicates.keys().__contains__(int(i)):
                        print(self.wrong)
                        is_valid_indexes = False
                        break
                    indexes.append(int(i))
                if is_valid_indexes:
                    print(indexes)
                    return indexes
            else:
                print(self.wrong)

    def __delete_files(self, indexes, files):
        total_bytes = 0
        for i in indexes:
            os.remove(files[i]['path'])
            total_bytes += int(files[i]['size'])
        print(f"Total freed up space: {total_bytes} bytes")


if __name__ == "__main__":
    args = sys.argv
    #args[1] == directory
    if len(args) == 1:
        print("Directory is not specified")
    else:
        Application(args[1]).run()
