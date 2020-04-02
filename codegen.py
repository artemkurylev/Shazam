import subprocess


def generate_code(path_to_binary, path_to_file):
    try:
        args = (path_to_binary, path_to_file)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()
        result = output.decode('utf_8')
        part = result.split('code"')[1]
        code = part.split('"')[1]
        return code
    except FileNotFoundError:
        print('Binary or audio file do not exist')


if __name__ == '__main__':
    print(generate_code('./echoprint-codegen', 'ib17_r1_Oxxxymiron_6702900.mp3'))
