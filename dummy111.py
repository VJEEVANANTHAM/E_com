# s="abcd"
# ls=[1,2,3]
# print(id(ls),ls)

# # print(id(s))
# ls=ls.append([1,2,3])

# s=""+"123"
# # ls[2]=1
# # print(id(s))
# print(id(ls),ls)


# l1=[1,3,5]
# l2=[2,4,6]

# l1_i=0
# l2_i=0

# lengh=len(l1)+len(l2)

# res=[]

# for each in range(lengh):
    
#     if l1[l1_i]<l2[l2_i]:
#         res.append(l1[l1_i])
#         l1_i+=1
#         # if l1_i == len(l1):
#         #     temp=l2[l2_i-1::]
#         #     res.extend(temp)
#         #     break
#     else:
#         res.append(l2[l2_i])
#         l2_i+=1
        
#         # if l2_i == len(l2):
#         #     temp=l1[l1_i-1::]
#         #     res.extend(temp)
            
#         #     break
        

# print(res)


# s="prograpppmming "

# res={}

# for char in s:
#     if char in res:
#         res[char]+=1
#     else:
#         res[char]=1
# print(res)

# c=s.count(s[0])
# print(f"{s[0]} : {c}")
    
# res={
#   "response": "Let's break down each technology and methodology, explaining what it is and why it's chosen in a modern development stack.\n\n---\n\n### **1. Python**\n\n*   **What it is:** A high-level, interpreted, general-purpose programming language known for its readability and versatility.\n*   **Why we want to use it:**\n    *   **Readability & Simplicity:** Its clear syntax allows developers to write less code and maintain it more easily, leading to faster development cycles.\n    *   **Vast Ecosystem & Libraries:** A massive collection of pre-built modules and frameworks (like FastAPI, libraries for data science, machine learning, web development, etc.) significantly accelerates development.\n    *   **Versatility:** Can be used for web development, data analysis, AI, automation, scripting, and more, making it a flexible choice for various parts of a project.\n    *   **Strong Community Support:** A large and active community provides extensive documentation, tutorials, and support, easing troubleshooting and learning.\n\n### **2. FastAPI**\n\n*   **What it is:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.\n*   **Why we want to use it:**\n    *   **High Performance:** Built on Starlette (for web parts) and Pydantic (for data validation), it's one of the fastest Python frameworks available, comparable to Node.js and Go.\n    *   **Automatic Interactive API Documentation:** Automatically generates OpenAPI (Swagger UI) and ReDoc documentation from your code, making it easy for frontend developers and other services to understand and consume the API.\n    *   **Data Validation & Serialization:** Leverages Pydantic for robust and automatic data validation, serialization, and deserialization, reducing boilerplate code and preventing common errors.\n    *   **Developer Experience:** Offers excellent editor support with type hints, leading to better code completion and error checking, improving developer productivity.\n    *   **Modern Features:** Supports asynchronous programming (`async/await`) out-of-the-box, allowing for efficient handling of concurrent requests.\n\n### **3. PostgreSQL**\n\n*   **What it is:** A powerful, open-source object-relational database system known for its reliability, feature robustness, and performance.\n*   **Why we want to use it:**\n    *   **Data Integrity & Reliability:** Adheres to ACID (Atomicity, Consistency, Isolation, Durability) properties, ensuring transactional reliability and data accuracy.\n    *   **Feature Richness:** Offers advanced features like JSON/JSONB support, full-text search, complex data types, and powerful indexing, making it versatile for various application needs.\n    *   **Scalability:** Highly scalable, capable of handling large volumes of data and concurrent users, supporting both vertical and horizontal scaling strategies.\n    *   **Extensibility:** Allows for custom functions, data types, and operators, enabling developers to tailor the database to specific requirements.\n    *   **Open Source & Community Support:** Free to use with a vibrant community, providing continuous improvements, security updates, and extensive support.\n\n### **4. Apache Kafka**\n\n*   **What it is:** A distributed streaming platform that enables you to publish, subscribe to, store, and process streams of records in real-time. It's designed for high-throughput, low-latency data feeds.\n*   **Why we want to use it:**\n    *   **Scalability & High Throughput:** Can handle millions of messages per second, making it ideal for processing large volumes of real-time data from various sources.\n    *   **Durability & Fault Tolerance:** Messages are persistently stored on disk and replicated across multiple brokers, ensuring data is not lost even if a server fails.\n    *   **Decoupling Services:** Acts as a central nervous system for microservices, allowing different applications to communicate asynchronously without direct dependencies, enhancing architectural flexibility.\n    *   **Real-time Data Processing:** Enables the building of event-driven architectures and real-time data pipelines, crucial for analytics, monitoring, and responsive user experiences.\n    *   **Ordered Message Delivery:** Guarantees message order within a partition, which is vital for many business processes.\n\n### **5. Unit Test**\n\n*   **What it is:** A software testing method where individual units or components of a software application are tested in isolation to determine if they are fit for use.\n*   **Why we want to use it:**\n    *   **Early Bug Detection:** Identifies defects in the smallest units of code early in the development cycle, when they are cheapest and easiest to fix.\n    *   **Improved Code Quality & Design:** Forces developers to write modular, decoupled, and testable code, leading to a better overall software design.\n    *   **Facilitates Refactoring:** Provides a safety net, allowing developers to make changes or refactor code with confidence that existing functionality is not broken.\n    *   **Living Documentation:** Unit tests serve as examples of how a particular function or method is intended to be used, acting as a form of executable documentation.\n    *   **Faster Feedback Loop:** Can be run quickly and frequently, providing immediate feedback on code changes.\n\n### **6. Docker**\n\n*   **What it is:** A platform for developing, shipping, and running applications in \"containers.\" Containers are lightweight, standalone, executable packages of software that include everything needed to run an application: code, runtime, system tools, libraries, and settings.\n*   **Why we want to use it:**\n    *   **Consistency Across Environments:** Solves the \"it works on my machine\" problem by packaging the application and its dependencies together, ensuring it runs identically from development to production.\n    *   **Isolation:** Each application runs in its own isolated container, preventing conflicts between different applications or their dependencies.\n    *   **Portability:** Containers can run on any system where Docker is installed (laptop, cloud server, data center), providing unparalleled portability.\n    *   **Faster Deployment & Scaling:** Standardizes the deployment process, making it quicker and more efficient to deploy, scale, and manage applications.\n    *   **Resource Efficiency:** Containers are much lighter than virtual machines, consuming fewer resources and allowing more applications to run on the same infrastructure.\n\n### **7. Bitbucket**\n\n*   **What it is:** A web-based version control repository hosting service, primarily for Git (and Mercurial) projects, provided by Atlassian.\n*   **Why we want to use it:**\n    *   **Version Control (Git Hosting):** Provides a centralized place to store and manage Git repositories, enabling tracking of all code changes, reverting to previous versions, and maintaining code history.\n    *   **Collaboration & Code Review:** Facilitates team collaboration through features like pull requests, code reviews, and inline commenting, ensuring code quality and knowledge sharing.\n    *   **Integrated CI/CD (Bitbucket Pipelines):** Offers built-in Continuous Integration/Continuous Delivery capabilities, allowing automation of builds, tests, and deployments directly within the platform.\n    *   **Access Control & Permissions:** Provides fine-grained control over repository access and permissions, ensuring code security and compliance.\n    *   **Integration with Atlassian Stack:** Seamlessly integrates with other Atlassian products like Jira (for project management) and Confluence (for documentation), creating a unified development ecosystem.\n\n### **8. Swagger (OpenAPI)**\n\n*   **What it is:** A set of open-source tools built around the OpenAPI Specification, which provides a standard, language-agnostic interface for REST APIs. Swagger UI specifically provides an interactive, browser-based documentation interface for APIs.\n*   **Why we want to use it:**\n    *   **Interactive API Documentation:** Automatically generates user-friendly, interactive documentation (Swagger UI) that allows developers to understand and even test API endpoints directly from their browser.\n    *   **API Contract Definition:** Provides a standardized way to define the structure of an API (endpoints, request/response formats, authentication), ensuring consistency and clear communication.\n    *   **Client & Server Code Generation:** The OpenAPI specification can be used to automatically generate client SDKs in various languages or even server stubs, significantly speeding up integration.\n    *   **API Design-First Approach:** Encourages designing the API contract before implementation, leading to more robust and well-thought-out API designs.\n    *   **Faster Onboarding:** New developers or external consumers can quickly understand and integrate with the API due to clear and up-to-date documentation.\n\n### **9. Postman**\n\n*   **What it is:** A popular API platform for building, testing, designing, and documenting APIs. It provides a user-friendly graphical interface for making HTTP requests and managing API workflows.\n*   **Why we want to use it:**\n    *   **API Development & Testing:** Simplifies sending various HTTP requests (GET, POST, PUT, DELETE, etc.), inspecting responses, and debugging API endpoints during development.\n    *   **Collaboration:** Allows teams to create, share, and organize collections of API requests, making it easy for multiple developers to work on and test APIs collaboratively.\n    *   **Test Automation:** Supports writing automated tests for API endpoints using JavaScript, enabling regression testing and ensuring API reliability.\n    *   **Mock Servers:** Can create mock servers to simulate API responses, allowing frontend development to proceed even if the backend API is not fully implemented.\n    *   **API Documentation:** Can generate API documentation from collections, providing another source of reference for API consumers.\n\n### **10. Agile**\n\n*   **What it is:** An iterative and incremental approach to software development that emphasizes collaboration, flexibility, continuous delivery, and customer feedback over rigid planning and extensive documentation.\n*   **Why we want to use it:**\n    *   **Adaptability to Change:** Embraces change throughout the development process, allowing teams to respond quickly to new requirements or market shifts.\n    *   **Faster Delivery of Value:** Focuses on delivering working software in short cycles (iterations), providing continuous value to the customer.\n    *   **Enhanced Customer Satisfaction:** Involves the customer throughout the process, ensuring the developed product truly meets their needs and expectations.\n    *   **Improved Quality:** Continuous testing and feedback loops lead to higher quality software with fewer defects.\n    *   **Better Collaboration & Communication:** Promotes close collaboration within the team and with stakeholders, fostering a shared understanding and transparency.\n\n### **11. Scrum**\n\n*   **What it is:** A lightweight, iterative, and incremental agile framework for managing complex product development. It organizes work into fixed-length iterations called \"Sprints\" (typically 1-4 weeks) and defines specific roles (Product Owner, Scrum Master, Development Team), events (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Increment).\n*   **Why we want to use it:**\n    *   **Structured Agility:** Provides a clear framework and set of rules that allow teams to implement Agile principles effectively without being overly prescriptive.\n    *   **Transparency & Visibility:** Daily Scrums, Sprint Reviews, and clear backlogs ensure everyone has a shared understanding of progress, impediments, and future work.\n    *   **Accountability & Focus:** Clearly defined roles and Sprint goals provide accountability and help the team stay focused on delivering specific increments of value.\n    *   **Continuous Improvement:** The Sprint Retrospective is a dedicated event for the team to inspect its processes and continuously improve its way of working.\n    *   **Predictability:** Fixed-length Sprints help in establishing a rhythm and improving the team's ability to forecast what can be delivered within an iteration."
# }
# print(res["response"])

"""

### **1. Python**

*   **What it is:** A high-level, interpreted, general-purpose programming language known for its readability and versatility.

*   **Why we want to use it:**
    
    *   **Readability & Simplicity:** Its clear syntax allows developers to write less code and maintain it more easily, leading to faster development cycles.
    
    *   **Vast Ecosystem & Libraries:** A massive collection of pre-built modules and frameworks (like FastAPI, libraries for data science, machine learning, 
        web development, etc.) significantly accelerates development.
    
    *   **Versatility:** Can be used for web development, data analysis, AI, automation, scripting, and more, making it a flexible choice for various parts of 
        a project.
    
    *   **Strong Community Support:** A large and active community provides extensive documentation, tutorials, and support, easing troubleshooting and learning.

### **2. FastAPI**

*   **What it is:** 
    
    A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

*   **Why we want to use it:**

    *   **High Performance:** Built on Starlette (for web parts) and Pydantic (for data validation), it's one of the fastest Python frameworks available, comparable 
        to Node.js and Go.
    
    *   **Automatic Interactive API Documentation:** Automatically generates OpenAPI (Swagger UI) and ReDoc documentation from your code, making it easy for frontend
        developers and other services to understand and consume the API.
    
    *   **Data Validation & Serialization:** Leverages Pydantic for robust and automatic data validation, serialization, and deserialization, reducing boilerplate code
        and preventing common errors.
    
    *   **Developer Experience:** Offers excellent editor support with type hints, leading to better code completion and error checking, improving developer productivity.
    
    *   **Modern Features:** Supports asynchronous programming (`async/await`) out-of-the-box, allowing for efficient handling of concurrent requests.

### **3. PostgreSQL**


*   **What it is:** A powerful, open-source object-relational database system known for its reliability, feature robustness, and performance.

*   **Why we want to use it:**
    
    *   **Data Integrity & Reliability:** Adheres to ACID (Atomicity, Consistency, Isolation, Durability) properties, ensuring transactional reliability and data accuracy.
    
    *   **Feature Richness:** Offers advanced features like JSON/JSONB support, full-text search, complex data types, and powerful indexing, making it versatile for 
        various application needs.
    
    *   **Scalability:** Highly scalable, capable of handling large volumes of data and concurrent users, supporting both vertical and horizontal scaling strategies.
    
    *   **Extensibility:** Allows for custom functions, data types, and operators, enabling developers to tailor the database to specific requirements.
    
    *   **Open Source & Community Support:** Free to use with a vibrant community, providing continuous improvements, security updates, and extensive support.

### **4. Apache Kafka**


*   **What it is:** A distributed streaming platform that enables you to publish, subscribe to, store, and process streams of records in real-time. It's designed for high-throughput, low-latency data feeds.

*   **Why we want to use it:**

    *   **Scalability & High Throughput:** Can handle millions of messages per second, making it ideal for processing large volumes of real-time data from various sources.

    *   **Durability & Fault Tolerance:** Messages are persistently stored on disk and replicated across multiple brokers, ensuring data is not lost even if a server fails.

    *   **Decoupling Services:** Acts as a central nervous system for microservices, allowing different applications to communicate asynchronously without direct dependencies, enhancing architectural flexibility.

    *   **Real-time Data Processing:** Enables the building of event-driven architectures and real-time data pipelines, crucial for analytics, monitoring, and responsive user experiences.

    *   **Ordered Message Delivery:** Guarantees message order within a partition, which is vital for many business processes.

### **5. Unit Test**

*   **What it is:** A software testing method where individual units or components of a software application are tested in isolation to determine if they are fit for use.

*   **Why we want to use it:**

    *   **Early Bug Detection:** Identifies defects in the smallest units of code early in the development cycle, when they are cheapest and easiest to fix.

    *   **Improved Code Quality & Design:** Forces developers to write modular, decoupled, and testable code, leading to a better overall software design.

    *   **Facilitates Refactoring:** Provides a safety net, allowing developers to make changes or refactor code with confidence that existing functionality is not broken.

    *   **Living Documentation:** Unit tests serve as examples of how a particular function or method is intended to be used, acting as a form of executable documentation.

    *   **Faster Feedback Loop:** Can be run quickly and frequently, providing immediate feedback on code changes.

### **6. Docker**


*   **What it is:** A platform for developing, shipping, and running applications in "containers." Containers are lightweight, standalone, executable packages of software that include everything needed to run an application: code, runtime, system tools, libraries, and settings.

*   **Why we want to use it:**

    *   **Consistency Across Environments:** Solves the "it works on my machine" problem by packaging the application and its dependencies together, ensuring it runs identically from development to production.

    *   **Isolation:** Each application runs in its own isolated container, preventing conflicts between different applications or their dependencies.

    *   **Portability:** Containers can run on any system where Docker is installed (laptop, cloud server, data center), providing unparalleled portability.

    *   **Faster Deployment & Scaling:** Standardizes the deployment process, making it quicker and more efficient to deploy, scale, and manage applications.

    *   **Resource Efficiency:** Containers are much lighter than virtual machines, consuming fewer resources and allowing more applications to run on the same infrastructure.

### **7. Bitbucket**


*   **What it is:** A web-based version control repository hosting service, primarily for Git (and Mercurial) projects, provided by Atlassian.

*   **Why we want to use it:**

    *   **Version Control (Git Hosting):** Provides a centralized place to store and manage Git repositories, enabling tracking of all code changes, reverting to previous versions, and maintaining code history.

    *   **Collaboration & Code Review:** Facilitates team collaboration through features like pull requests, code reviews, and inline commenting, ensuring code quality and knowledge sharing.

    *   **Integrated CI/CD (Bitbucket Pipelines):** Offers built-in Continuous Integration/Continuous Delivery capabilities, allowing automation of builds, tests, and deployments directly within the platform.

    *   **Access Control & Permissions:** Provides fine-grained control over repository access and permissions, ensuring code security and compliance.

    *   **Integration with Atlassian Stack:** Seamlessly integrates with other Atlassian products like Jira (for project management) and Confluence (for documentation), creating a unified development ecosystem.

### **8. Swagger (OpenAPI)**

*   **What it is:** A set of open-source tools built around the OpenAPI Specification, which provides a standard, language-agnostic interface for REST APIs. Swagger UI specifically provides an interactive, browser-based documentation interface for APIs.

*   **Why we want to use it:**

    *   **Interactive API Documentation:** Automatically generates user-friendly, interactive documentation (Swagger UI) that allows developers to understand and even test API endpoints directly from their browser.

    *   **API Contract Definition:** Provides a standardized way to define the structure of an API (endpoints, request/response formats, authentication), ensuring consistency and clear communication.

    *   **Client & Server Code Generation:** The OpenAPI specification can be used to automatically generate client SDKs in various languages or even server stubs, significantly speeding up integration.

    *   **API Design-First Approach:** Encourages designing the API contract before implementation, leading to more robust and well-thought-out API designs.

    *   **Faster Onboarding:** New developers or external consumers can quickly understand and integrate with the API due to clear and up-to-date documentation.

### **9. Postman**

*   **What it is:** A popular API platform for building, testing, designing, and documenting APIs. It provides a user-friendly graphical interface for making HTTP requests and managing API workflows.

*   **Why we want to use it:**

    *   **API Development & Testing:** Simplifies sending various HTTP requests (GET, POST, PUT, DELETE, etc.), inspecting responses, and debugging API endpoints during development.

    *   **Collaboration:** Allows teams to create, share, and organize collections of API requests, making it easy for multiple developers to work on and test APIs collaboratively.

    *   **Test Automation:** Supports writing automated tests for API endpoints using JavaScript, enabling regression testing and ensuring API reliability.

    *   **Mock Servers:** Can create mock servers to simulate API responses, allowing frontend development to proceed even if the backend API is not fully implemented.

    *   **API Documentation:** Can generate API documentation from collections, providing another source of reference for API consumers.

### **10. Agile**

*   **What it is:** An iterative and incremental approach to software development that emphasizes collaboration, flexibility, continuous delivery, and customer feedback over rigid planning and extensive documentation.

*   **Why we want to use it:**

    *   **Adaptability to Change:** Embraces change throughout the development process, allowing teams to respond quickly to new requirements or market shifts.

    *   **Faster Delivery of Value:** Focuses on delivering working software in short cycles (iterations), providing continuous value to the customer.

    *   **Enhanced Customer Satisfaction:** Involves the customer throughout the process, ensuring the developed product truly meets their needs and expectations.

    *   **Improved Quality:** Continuous testing and feedback loops lead to higher quality software with fewer defects.

    *   **Better Collaboration & Communication:** Promotes close collaboration within the team and with stakeholders, fostering a shared understanding and transparency.

### **11. Scrum**

*   **What it is:** A lightweight, iterative, and incremental agile framework for managing complex product development. It organizes work into fixed-length iterations called "Sprints" (typically 1-4 weeks) and defines specific roles (Product Owner, Scrum Master, Development Team), events (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Increment).

*   **Why we want to use it:**

    *   **Structured Agility:** Provides a clear framework and set of rules that allow teams to implement Agile principles effectively without being overly prescriptive.

    *   **Transparency & Visibility:** Daily Scrums, Sprint Reviews, and clear backlogs ensure everyone has a shared understanding of progress, impediments, and future work.

    *   **Accountability & Focus:** Clearly defined roles and Sprint goals provide accountability and help the team stay focused on delivering specific increments of value.

    *   **Continuous Improvement:** The Sprint Retrospective is a dedicated event for the team to inspect its processes and continuously improve its way of working.

    *   **Predictability:** Fixed-length Sprints help in establishing a rhythm and improving the team's ability to forecast what can be delivered within an iteration.
"""


# # from datetime import datetime,time,date
# import datetime,time


# today=datetime.datetime.today().timestamp()

# time_delta=datetime.timedelta(2)
# print(today)
# # print(time_delta)

# from appium import webdriver
# from appium.options.android import UiAutomator2Options
# import time

# def launch_youtube_with_appium():
#     # 1. Define Appium configuration capabilities
#     options = UiAutomator2Options()
    
#     # Core connection capabilities
#     options.platform_name = 'Android'
#     options.automation_name = 'UiAutomator2'
    
#     # REPLACE THIS with your actual device ID from 'adb devices'
#     options.device_name = 'YOUR_DEVICE_ID_HERE' 
    
#     # Direct Appium to open the YouTube application specifically
#     options.app_package = 'com.google.android.youtube'
#     options.app_activity = 'com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity'
    
#     # Ensures your phone doesn't reset or clear Appium caches every run
#     options.no_reset = True 

#     # 2. Connect to the local running Appium Server
#     print("Connecting to Appium Server and waking up device...")
#     appium_server_url = 'http://127.0.0.1:4723'
#     driver = webdriver.Remote(appium_server_url, options=options)

#     try:
#         print("YouTube opened successfully!")
        
#         # Keep it open for 10 seconds to watch it happen
#         time.sleep(10)
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
        
#     finally:
#         # 3. Always quit the session to release your device resources cleanly
#         print("Closing Appium session...")
#         driver.quit()

# if __name__ == "__main__":
#     launch_youtube_with_appium()


import webbrowser
import time

url = "http://127.0.0.1:8000/payment"

for i in range(3):
    webbrowser.open_new_tab(url)
    time.sleep(0.2)  # small delay between tabs
url="http://127.0.0.1:8000/profile"
for i in range(2):
    webbrowser.open_new_tab(url)
    time.sleep(0.5)  # small delay between tabs
