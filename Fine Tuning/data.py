def get_data():
    data = [
    {
        "input": "What is Cloud Native Applied Generative AI Engineering?",
        "output": "It's the application of generative AI technologies to solve real-world problems in the cloud."
    },
    {
        "input": "How valuable are Cloud Native Applied Generative AI developers?",
        "output": "They are in high demand due to the increasing adoption of GenAI technologies across various industries."
    },
    {
        "input": "What is the potential for Cloud Applied Generative AI Developers to start their own companies?",
        "output": "They have a significant potential due to the emerging field, market demand, innovation and differentiation, access to cloud resources, entrepreneurial opportunities, and collaboration and partnerships."
    },
    {
        "input": "Is the program not too long, one year is a long time?",
        "output": "The program is one year long and covers a wide range of topics including Python, Front-end Development, GenAI, API, Database, Cloud Development, and DevOps."
    },
    {
        "input": "Why don't we use TypeScript (Node.js) to develop APIs instead of using Python?",
        "output": "Python is the de facto standard for AI development and has a larger ecosystem of libraries and frameworks available, especially for AI."
    },
    {
        "input": "What is the difference between OpenAI Completion API, OpenAI Assistant API, Google Gemini Multi-Modal API, and LangChain?",
        "output": "They are different ways of using artificial intelligence to generate text, images, audio, and video based on some input, but they have different features and applications."
    },
    {
        "input": "Why don't we use Flask or Django for API development instead of FastAPI?",
        "output": "FastAPI is a newer and more modern framework than Flask or Django. It is designed to be fast, efficient, and easy to use."
    },
    {
        "input": "Why do we need to learn Cloud technologies in a Generative AI program?",
        "output": "Cloud technologies provide a scalable and reliable platform for hosting and managing complex workloads."
    },
    {
        "input": "What is the purpose of Docker Containers and what are the benefits of deploying them with Docker Compose and Kubernetes?",
        "output": "Docker Containers are a way to package software into a single unit that can be run on any machine. Docker Compose allows you to define and manage multi-container Docker applications locally. Kubernetes automates the deployment, scaling, and management of containerized applications."
    },
    {
        "input": "What is the purpose of learning to develop APIs in a Generative AI program?",
        "output": "APIs are used to connect different software applications and services together. They are the building blocks of the internet and are essential for the exchange of data between different systems."
    },
    {
        "input": "What is the purpose of using Python-based FastAPI and related technologies in Quarter 2?",
        "output": "FastAPI is a high-performance, lightweight, and easy-to-use framework for building APIs. Students will also learn about Pydantic, SQLModel, and PostgreSQL."
    },
    {
        "input": "What does the API-as-a-Product model entail?",
        "output": "API-as-a-Product is a type of Software-as-a-Service that monetizes niche functionality, typically served over HTTP. In this model, the API is at the core of the business's value."
    },
    {
        "input": "What are the benefits of using Docker Containers for development, testing, and deployment?",
        "output": "Docker Containers provide a consistent environment that can be used across different systems. This eliminates the need to worry about dependencies or compatibility issues, and it can help to improve the efficiency of the development process."
    },
    {
        "input": "Why in this program are we not learning to build LLMs ourselves? How difficult is it to develop an LLM like ChatGPT 4 or Google's Gemini?",
        "output": "Developing an LLM like ChatGPT 4 or Google Gemini is extremely difficult and requires a complex combination of resources, expertise, and infrastructure."
    },
    {
        "input": "Business wise does it make more sense to develop LLMs ourselves from scratch or use LLMs developed by others and build applications using these tools by using APIs and/or fine-tuning them?",
        "output": "Whether it makes more business sense to develop LLMs from scratch or leverage existing ones through APIs and fine-tuning depends on several factors specific to your situation."
    },
    {
        "input": "What are Custom GPTs?",
        "output": "Custom GPTs are specialized versions of the Generative Pre-trained Transformer (GPT) models that are tailored for specific tasks, industries, or data types."
    },
    {
        "input": "What are Actions in GPTs?",
        "output": "Actions are a way to connect custom GPTs to external APIs, allowing them to access data or interact with the real-world."
    },
    {
        "input": "What are the different specialisations offered at the end of the program and what are their benefits?",
        "output": "The program offers six specialisations in different fields: Healthcare and Medical GenAI, Web3, Blockchain, and GenAI Integration, Metaverse, 3D, and GenAI Integration, GenAI for Accounting, Finance, and Banking, GenAI for Engineers, GenAI for Sales and Marketing, and GenAI for Automation and Internet of Things (IoT), GenAI for Cyber Security."
    },
    {
        "input": "What is the focus of the program?",
        "output": "The focus of the program is not on LLM model development but on applied Cloud GenAI Engineering (GenEng), application development, and fine-tuning of foundational models."
    },
    {
        "input": "Why is it important to learn about cloud technologies?",
        "output": "Cloud technologies provide a scalable and reliable platform for hosting and managing complex workloads."
    },
    {
        "input": "What specific Python libraries and frameworks will be covered in the program, beyond FastAPI?",
        "output": "The program will cover libraries and frameworks like SQLModel, Postgres, Kafka, Kong, OpenAI, Open Source AI LLMs, Docker, DevContainers, TestContainers, Kubernetes, Terraform, PyTorch, Power BI, Langchain, and CrewAl."
    },
    {
        "input": "How will the program incorporate real-world projects or case studies to enhance practical learning?",
        "output": "The program will incorporate real-world projects and case studies throughout the curriculum to provide students with practical experience in applying their skills to solve real-world problems."
    },
    {
        "input": "What are the specific learning outcomes or skills students are expected to acquire by the end of each quarter?",
        "output": "The program outlines specific learning outcomes and skills for each quarter, covering topics like Python programming, cloud native microservices development, distributed system design, custom GPTs and multi-AI agent systems, cloud native AI and business intelligence, and front-end web GUI development."
    },
    {
        "input": "How will the program address the ethical considerations and potential biases associated with generative AI?",
        "output": "The program will incorporate discussions and exercises on ethical considerations and potential biases associated with generative AI, ensuring students understand the responsible development and deployment of AI solutions."
    },
    {
        "input": "What are the opportunities for mentorship or networking with industry professionals within the program?",
        "output": "The program offers opportunities for mentorship and networking with industry professionals through guest lectures, workshops, and industry events."
    },
    {
        "input": "How will the program prepare students for the specific requirements of the Cloud Native Applied Generative AI certification?",
        "output": "The program is designed to prepare students for the specific requirements of the Cloud Native Applied Generative AI certification, covering the necessary skills and knowledge for the exam."
    },
    {
        "input": "What are the typical career paths or job roles that graduates of this program are expected to pursue?",
        "output": "Graduates of this program are expected to pursue career paths as Cloud Native Applied Generative AI Engineers, AI Developers, AI Architects, AI Consultants, and AI Researchers."
    },
    {
        "input": "How will the program integrate the use of Docker containers, Docker Compose, and Kubernetes for practical application development?",
        "output": "The program will provide hands-on experience in using Docker containers, Docker Compose, and Kubernetes for deploying and managing cloud-native applications."
    },
    {
        "input": "What are the specific examples of open-source LLMs and AI APIs that will be explored in the program?",
        "output": "The program will explore open-source LLMs like OpenAI's GPT-3 and Google's Gemini, and AI APIs like OpenAI's Completion API, Assistant API, and Google Gemini Multi-Modal API."
    },
    {
        "input": "How will the program incorporate the use of design thinking and behavior-driven development (BDD) in the creation of AI solutions?",
        "output": "The program will integrate design thinking and BDD methodologies to help students create AI solutions that are user-centric and aligned with real-world needs."
    },
    {
        "input": "What are the specific tools and techniques that will be covered for visualizing data using Power BI in the program?",
        "output": "The program will cover tools and techniques for data visualization using Power BI, enabling students to create interactive dashboards and reports for analyzing data."
    },
    {
        "input": "How will the program address the potential challenges of integrating generative AI with existing business processes and systems?",
        "output": "The program will provide guidance and practical examples on how to integrate generative AI with existing business processes and systems, addressing challenges related to data integration, workflow automation, and user adoption."
    },
    {
        "input": "What are the specific examples of cloud platforms and services that will be used in the program, such as Azure, Google Cloud, and AWS?",
        "output": "The program will utilize cloud platforms and services like Azure, Google Cloud, and AWS for deploying and managing cloud-native applications and AI workloads."
    },
    {
        "input": "How will the program help students develop the necessary skills for building and deploying custom GPTs and multi-AI agent systems?",
        "output": "The program will provide hands-on experience in building and deploying custom GPTs and multi-AI agent systems using OpenAI's API and other tools, enabling students to create AI systems tailored for specific tasks and industries."
    },
    {
        "input": "What are the specific examples of open-source libraries like Langchain and CrewAl that will be used for automating tasks in the program?",
        "output": "The program will utilize open-source libraries like Langchain and CrewAl for automating tasks, enabling students to create AI-powered workflows for repetitive tasks and business processes."
    },
    {
        "input": "How will the program address the potential challenges of integrating generative AI with existing business processes and systems?",
        "output": "The program will provide guidance and practical examples on how to integrate generative AI with existing business processes and systems, addressing challenges related to data integration, workflow automation, and user adoption."
    },
    {
        "input": "What are the specific examples of cloud platforms and services that will be used in the program, such as Azure, Google Cloud, and AWS?",
        "output": "The program will utilize cloud platforms and services like Azure, Google Cloud, and AWS for deploying and managing cloud-native applications and AI workloads."
    },
    {
        "input": "How will the program help students develop the necessary skills for building and deploying custom GPTs and multi-AI agent systems?",
        "output": "The program will provide hands-on experience in building and deploying custom GPTs and multi-AI agent systems using OpenAI's API and other tools, enabling students to create AI systems tailored for specific tasks and industries."
    },
    {
        "input": "What are the specific examples of open-source libraries like Langchain and CrewAl that will be used for automating tasks in the program?",
        "output": "The program will utilize open-source libraries like Langchain and CrewAl for automating tasks, enabling students to create AI-powered workflows for repetitive tasks and business processes."
    },
    {
        "input": "How will the program address the potential challenges of integrating generative AI with existing business processes and systems?",
        "output": "The program will provide guidance and practical examples on how to integrate generative AI with existing business processes and systems, addressing challenges related to data integration, workflow automation, and user adoption."
    },
    {
        "input": "What are the specific examples of cloud platforms and services that will be used in the program, such as Azure, Google Cloud, and AWS?",
        "output": "The program will utilize cloud platforms and services like Azure, Google Cloud, and AWS for deploying and managing cloud-native applications and AI workloads."
    },
    {
        "input": "How will the program help students develop the necessary skills for building and deploying custom GPTs and multi-AI agent systems?",
        "output": "The program will provide hands-on experience in building and deploying custom GPTs and multi-AI agent systems using OpenAI's API and other tools, enabling students to create AI systems tailored for specific tasks and industries."
    },
    {
        "input": "What are the specific examples of open-source libraries like Langchain and CrewAl that will be used for automating tasks in the program?",
        "output": "The program will utilize open-source libraries like Langchain and CrewAl for automating tasks, enabling students to create AI-powered workflows for repetitive tasks and business processes."
    },
    {
        "input": "How will the program address the potential challenges of integrating generative AI with existing business processes and systems?",
        "output": "The program will provide guidance and practical examples on how to integrate generative AI with existing business processes and systems, addressing challenges related to data integration, workflow automation, and user adoption."
    },
    {
        "input": "What are the specific examples of cloud platforms and services that will be used in the program, such as Azure, Google Cloud, and AWS?",
        "output": "The program will utilize cloud platforms and services like Azure, Google Cloud, and AWS for deploying and managing cloud-native applications and AI workloads."
    },
    {
        "input": "How will the program help students develop the necessary skills for building and deploying custom GPTs and multi-AI agent systems?",
        "output": "The program will provide hands-on experience in building and deploying custom GPTs and multi-AI agent systems using OpenAI's API and other tools, enabling students to create AI systems tailored for specific tasks and industries."
    },
]
    return data