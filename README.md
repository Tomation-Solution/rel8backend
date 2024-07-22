# Rel8 Backend APIs

## Features

- Onboarding of Administrators as super admin to create members via excel sheet


## Getting Started

### Prerequisites

- Python 3.7+ install

### Installation

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Tomation-Solution/rel8backend.git
   cd rel8backend


2.  **Create Virtual Environment and Install Requirements**
    ```bash
        python3 -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Run and Execute Migration Script**

    ```
         ##Make the script executable by
         chmod +x release.sh
        ./release.sh
    ```

5. **Start Server**

    ```bash
        python3 manage.py runserver
    ```
