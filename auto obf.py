import subprocess
import os

#input the storm obf.py file with the mal.py as a malware before you execute 
def obfuscate(input_file, iterations=6):
    current_input = input_file

    for i in range(1, iterations + 1):
        output_file = f"mal{i+1}.py"
        print(f"Obfuscating {current_input} -> {output_file}")
        result = subprocess.run(
            ["python", "obf_py.py", "-i", current_input, "-o", output_file, "-r", "2", "--include-imports"],
            shell=True
        )
        if result.returncode != 0:
            print(f"Error during obfuscation at iteration {i}. Exiting.")
            break

        current_input = output_file

        if os.path.exists(current_input) and i > 1:
            os.remove(f"mal{i}.py")

def entry():
    try:
        times = int(input("Enter the number of obfuscation iterations (10-30): "))
        if 10 <= times <= 30:
            obfuscate("mal.py", iterations=times)
        else:
            print("Invalid input. Please enter a number between 10 and 30.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    entry()
