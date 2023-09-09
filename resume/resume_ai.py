"""
Wrapper for the OpenAI API calls
"""

import openai
import os
import builtins
import re
from enum import Enum

DEBUG = True


# override print function to print only in debug mode
def print(*args, **kwargs):
    if DEBUG:
        builtins.print(*args, **kwargs)


class ResumeAIRole(Enum):
    HR = 0
    APPLICANT = 1

    def description(self):
        if self == ResumeAIRole.HR:
            return "You are the principal HR (Human Resources)/recruiter of a company."
        elif self == ResumeAIRole.APPLICANT:
            return "You are a candidate applying for a new job."
        raise ValueError("Invalid role")


class ResumeAI:
    """
    OpenAI with custom instructions
    """

    def __init__(self, role: ResumeAIRole) -> None:
        with open(f"{os.path.dirname(__file__)}/openai.key") as f:
            key = f.read().strip()
        openai.api_key = key
        print("OpenAI API key loaded with role:", role)
        self._role: ResumeAIRole = role

    def ask(self, message: str) -> str:
        """
        Ask a question to the AI
        """
        role_description = self._role.description()

        final_message = f"{role_description}\n{message}"
        response = self._ask_turbo(final_message)
        output = response["choices"][0]["message"]["content"]
        # print token used
        print("OpenAI token used:", response["usage"]["total_tokens"])
        return output.strip()

    def review(self, resume: str, job_post: str) -> str:
        """
        Review a resume from different perspectives
        """
        role_description = self._role.description()

        final_message = (
            self._build_message(role_description, resume, job_post) + "###\n"
        )
        response = self._ask_turbo(final_message)
        return self._retrieve_output(response)

    def score(self, resume: str, job_post: str) -> str:
        """
        Rate the resume based on the job post depending on closely the resume matches the job post
        """
        role_description = self._role.description()

        final_message = (
            self._build_message(role_description, resume, job_post)
            + "Based on the give information, how would you rate this resume based on how relavent with the job post? (1 - 100)\n"
            + "Only output the number without any other text."
        )
        response = self._ask_turbo(final_message)
        return self._retrieve_output(response)

    def rewrite(self, resume: str, job_post: str) -> str:
        """
        Rewrite the resume based on the job post
        """
        role_description = self._role.description()

        final_message = (
            self._build_message(role_description, resume, job_post)
            + "Rewrite the resume based on the job post if there is a match.\nGenerate the new resume in a clear format without following its original style.\nApply proper spacing and indentation.\n"
            + "Output in the MarkDown format without any other text starting with # Resume"
        )
        response = self._ask_turbo(final_message)
        markdown = self._retrieve_output(response)
        with open("resume/new_resume.md", "w", encoding="utf-8") as f:
            f.write(markdown)
        return markdown

    def _build_message(self, role_description: str, resume: str, job_post: str) -> str:
        """
        Build the message to send to the AI
        """
        language_detection = (
            "Identify the text language of the resume section. Language means English, Chinese, Japanese or any spoken languages.\n"
            + "Update the resume's text language (English, Chinese, etc.) to match the job post's language. Output the using result in the job post's text language\n###\n"
        )
        return f"{language_detection}{role_description}\n###\nResume:\n{resume}\n###\nJob post:\n{job_post}\n###\n"

    def _ask_turbo(self, message: str) -> dict:
        """
        Ask a question to the AI with the turbo engine
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "assistant",
                    "content": message,
                },
            ],
        )
        return response

    def _retrieve_output(self, response: dict) -> str:
        """
        Retrieve the output from the response
        """
        return response["choices"][0]["message"]["content"].strip()

    def shrink_input(self, message: str) -> str:
        """
        Remove extra spaces and newlines
        """
        return re.sub(r"\s+", " ", message).strip()


if __name__ == "__main__":
    from resume_extract import extract_resume

    resume = ResumeAI(ResumeAIRole.APPLICANT)
    # print(resume.ask("おなまえは？"))
    # exit()

    # review
    my_resume = extract_resume("resume/resume.pdf")
    my_resume = resume.shrink_input(my_resume)
    with open("resume/job_post.txt", encoding="utf-8") as f:
        job_post = f.read()
    job_post = resume.shrink_input(job_post)
    # print(resume.review(my_resume, job_post))

    # # score
    # print(resume.score(my_resume, job_post))

    # rewrite
    print(resume.rewrite(my_resume, job_post))
