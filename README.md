# Better Resume Maybe

Use magic to help with resume.

No guarantee of anything. Use at your own risk. Don't take what AI says seriously.

## Setup

There are three additional files required to place under `resume/`:

- `job_post.txt` for the job description, simply copy and paste the job description into this file
- `resume.pdf` for your resume, the program will extract all texts from the pdf file
- `openai.key` for the OpenAI API key, you can get one from [here](https://platform.openai.com/account/api-keys)

However, the PDF is not a hard requirement. The program simply needs your resume in the TXT format. It is better if you simply copy all the text from your resume.

## Usage

Now, setup the virtual environment and install the dependencies:

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Simply, run the program:

```bash
python3 resume/resume_ai.py
```

The program can be fully customised by changing the `resume/resume_ai.py` file. You can add a new role with a description, use `custom` to build your custom instruction.
