#!/usr/bin/python3

import subprocess



def main(args=None):
    result = subprocess.run(["ls", "/"], stderr=subprocess.PIPE, text=True)
    print(result.stderr)

    bashCommand = "ls -l"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)


if __name__ == '__main__':
    main()