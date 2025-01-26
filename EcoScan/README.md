# EcoScan

EcoScan is a web platform that empowers users to make eco-friendly choices by guiding them through recycling, tree planting, and sustainability. With features such as AI-powered image validation, a tree rewards system, and personalized recycling tips, EcoScan aims to create a more sustainable world through education and action.

## Inspiration
EcoScan was inspired by the need for sustainable solutions in our everyday lives. We wanted to provide a platform where users could learn about recycling, plant trees, and make a positive environmental impact. Our goal is to encourage responsible actions for the environment and empower people to contribute to tree growth while earning rewards.

#### Notebook can be found in [`EcoScan/recycle.ipynb`](https://github.com/AfreenInnovates/AI-Hack/blob/main/EcoScan/recycle.ipynb)

## What it does
- **Sign Up/Login**: Users can create personalized accounts to track their progress and rewards.
- **Recycling Tips**: Upload images of items for AI-powered recycling tips based on how to recycle or dispose of them.
- **Tree Rewards**: Users can upload images of trees they've planted and receive rewards for contributing to environmental sustainability.
- **Image Validation**: The AI validates whether the uploaded image is of a plant or tree, and scores are given accordingly.
- **Delete Trees**: Users can delete trees from their collection, which will lower their rewards.
- **Quiz**: Take a quiz to discover which organizations align with your interests for donations or volunteer opportunities.

## How we built it
EcoScan was developed using a variety of technologies:
- **Backend**: Flask (Python) to build the web application and handle server-side logic.
- **Frontend**: HTML, CSS, and JavaScript for the user interface and interaction.
- **Database**: SQLAlchemy with SQLite to manage user accounts, uploaded images, and rewards.
- **AI/ML**: Gemini AI models for image recognition, and also built models from scratch, receiving accuracy of 94%: classification between organic and recyclable.
- **Machine Learning Frameworks**: PyTorch, TensorFlow, and FastAI for model building and training.
- **TinType**: Used TinType for project management, keeping a track of tasks completed, and integrating with Trello to make workflow easier.

## Challenges we ran into
- **Backend Integration**: One of the main challenges was integrating the backend system to handle user accounts and manage the database efficiently using SQLAlchemy and SQLite.
- **Image Recognition**: Ensuring that the AI model could accurately validate plant/tree images presented some difficulties, especially regarding the model’s ability to detect and classify images with high accuracy.
- **Database Management**: Setting up the database schema to store user data and image records posed challenges, especially as we scaled the platform.

## Accomplishments that we're proud of
- Built an AI-powered platform that provides users with **personalized recycling tips** based on uploaded images.
- Developed a **tree rewards system**, allowing users to earn points and rewards by planting trees and uploading images.
- Created a **quiz feature** that helps users find suitable organizations for donations or volunteering.
- Set the foundation for future **collaborations with environmental organizations** to promote sustainability further.

## What we learned
- **Backend Development**: Gained a solid understanding of how to manage user accounts and interact with databases using SQLAlchemy and SQLite.
- **AI & ML Integration**: Learned how to integrate **computer vision models** for image validation and how to leverage **HuggingFace** models for providing actionable recycling tips.
- **Database Management**: Developed skills in designing databases and handling large-scale data operations within Python.
- **Technical Growth**: We enhanced our skills in machine learning, AI model training (PyTorch, TensorFlow), and the application of modern Python libraries.

## What's next for EcoScan
- **Collaboration with Organizations**: We're wanting to go on partnerships with eco-friendly organizations, offering users incentives such as **gift cards** and **swag** for planting trees and getting involved.
- **Expanded AI Capabilities**: Plan to enhance the **image recognition model** to increase accuracy and handle more diverse plant/tree images. Use models from HuggingFace or train more advanced models!
- **Recycling Education**: Extend the platform's capabilities to offer more **detailed and contextual recycling tips** using advanced AI-powered language models.
- **Wider Impact**: We envision EcoScan inspiring **global tree planting efforts**, with more people participating in tree planting and sustainable living practices.

### Future Plans
- **User Engagement**: Offer rewards for users who plant multiple trees, such as **gift cards** for eco-friendly products or food items.
- **Machine Learning Advancements**: Integrate more advanced **computer vision models** and AI techniques to improve the accuracy of image classification.
- **Sustainability Partnerships**: Collaborate with environmental groups and organizations to further expand EcoScan’s impact on global sustainability efforts.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLAlchemy, SQLite
- **AI & Machine Learning**: Gemini AI, PyTorch, TensorFlow, FastAI
