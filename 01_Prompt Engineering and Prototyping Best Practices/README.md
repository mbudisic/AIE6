<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 1: Introduction and Vibe Check</h1>

### [Quicklinks](https://github.com/AI-Maker-Space/AIE6/tree/main/00_AIM_Quicklinks)

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|
| [Session 1: Pre-Work](https://www.notion.so/Session-1-Introduction-and-Vibe-Check-1c8cd547af3d81b596bbdfb64cf4fd2f?pvs=4#1c8cd547af3d81fb96b4f625f3f8e3d6)| [Session 1: Introduction and Vibe Check](https://www.notion.so/Session-1-Introduction-and-Vibe-Check-1c8cd547af3d81b596bbdfb64cf4fd2f) | Coming Soon! | Coming Soon! | You Are Here! | [Homework](https://forms.gle/W59zjs5MQc7kbLUh9) | [AIE6 Feedback 4/1](https://forms.gle/EdzBz82yGqVYKfUw9)

### Assignment

In the following assignment, you are required to take the app that you created for the AIE6 challenge (from [this repository](https://github.com/AI-Maker-Space/Beyond-ChatGPT)) and conduct what is known, colloquially, as a "vibe check" on the application.

You will be required to submit a link to your GitHub, as well as screenshots of the completed "vibe checks" through the provided Google Form!

> NOTE: This will require you to make updates to your personal class repository, instructions on that process can be found [here](https://github.com/AI-Maker-Space/AIE6/tree/main/00_Setting%20Up%20Git)!

#### How AIM Does Assignments

Throughout our time together - we'll be providing a number of assignments. Each assignment can be split into two broad categories:

- Base Assignment - a more conceptual and theory based assignment focused on locking in specific key concepts and learnings.
- Hardmode Assignment - a more programming focused assignment focused on core code-concepts.

Each assignment will have a few of the following categories of exercises:

- ❓Questions - these will be questions that you will be expected to gather the answer to! These can appear as general questions, or questions meant to spark a discussion in your breakout rooms!
- 🏗️ Activities - these will be work or coding activities meant to reinforce specific concepts or theory components.
- 🚧 Advanced Builds - these will only appear in Hardmode assignments, and will require you to build something with little to no help outside of documentation!

##### 🏗️ Activity #1

Please evaluate your system (`gpt-turbo-3.5`) on the following questions:

1. Explain the concept of object-oriented programming in simple terms to a complete beginner.

    - Aspect Tested:

> Aspect: Explanation of technical information contained out-of-context in a particular style. Conceptually, the answer is not incorrect (from a perspective of a writing for a non-technical person), but the style is not great - it is following the step-by-step approach too literally, assigning its sentences to steps even though it is not describing a procedure.

2. Read the following paragraph and provide a concise summary of the key points:

> Aspect Tested: Summarization of in-context information. The summary is very good, and the additional explanation of what "concise" means that I added to the prompt template is followed. Pretty happy with this result.

3. Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.

> Aspect Tested: Generation of non-technical information in an engaging way; 
> empathy (it has to interpret what is unexpected to humans). The story is 
> not bad, about two robots Spark and Whiz. It reads as a summary of a
> pilot for a kids cartoon. If I had to answer this prompt myself, I'm not sure
> that I'd do much better.

4. If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?

> Aspect Tested: Extracting mathematics from word-problem; solving the mathematical problem.
> The answer is succinct and correct, with consistent use of the information throughout the answer.
> Word-problem is interpreted well and the explanation is good enough.

5. Rewrite the following paragraph in a professional, formal tone…

> Aspect Tested: I had it rewrite "My Adidas" by Run DMC! It did OK, but it was using floral language
> a bit too often ("traverse" instead of "walk"). It's struggling with simplifying stylistic phrases (it repeats "touch the sand" even though a person formalizing this would use a less floral phrase).

6. (Added!) Convert the following recursion written in C into a flat for loop in Python:

> Aspect: code assistant. It does not output Python code (like some later models) but it does explain correctly how to convert recursive code into a loop. The answer is like a TA would give to an undergrad in a lab - not giving away the full solution, but guiding toward it. Uses step-by-step reasoning. All in all, good, but does not complete the request to code it in Python (the answer is generic to any declarative language).

7. (Added!) You are on an island where some people always tell the truth and some always lie. You meet two islanders:
    Alice says, “Bob is a liar.”
    Bob says, “We are both truth-tellers.”

    Who is telling the truth?

    > Aspect: deduction. It fails miserably - its interpretation of logic is inconsistent from sentence to sentence, it doesn't apply logical rules correctly (negation of AND results in OR of negatives) and so on. Would not recommend.

This "vibe check" now serves as a baseline, of sorts, to help understand what holes your application has.

##### 🚧 Advanced Build

Please make adjustments to your application that you believe will improve the vibe check done above, push the changes to your HF Space and redo the above vibe check.

> Here's the [updated app running on HF](https://huggingface.co/spaces/mbudisic/llm-app) and [the loom video](https://www.loom.com/share/0311a7b539ee4e75bea5e2a04c4ff5b8?sid=bfe99ce4-52ed-4198-a7c3-3e774f4af85b) - discussion thread is on [#build-ship-share](https://discord.com/channels/1135695983720792216/1135700320517890131/1357344146762760202):
>
> Changes to the "stock" chainlit app:
>
> 1. Added buttons that automate vibe checking prompts.
> 1. Added env variable `BEYOND_MODEL` that allows changing the model.
> 1. Updated the prompt template according to Bsharat et al. (2024)
> 1. Added two vibe check prompts: code translation/rewrite and logic.

### A Note on Vibe Checking

"Vibe checking" is an informal term for cursory unstructured and non-comprehensive evaluation of LLM-powered systems. The idea is to loosely evaluate our system to cover significant and crucial functions where failure would be immediately noticeable and severe.

In essence, it's a first look to ensure your system isn't experiencing catastrophic failure.

##### 🧑‍🤝‍🧑❓ Discussion Question #1

What are some limitations of vibe checking as an evaluation tool?

> 1. The judgement about the response quality is subjective.
> 1. It is not reliably reproducible - even when temperature of the model is
> set to 0, there is still stochasticity remaining.
> 1. It depends on the prompting skill of the user (so the test evaluates
> the user-assistant pairing, not assistant in isolation).
