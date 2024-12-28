# Odoo Employee Termination Module

The Odoo Employee Termination Module is designed to manage the termination process of employees within your organization. It provides a structured workflow for processing employee resignations and allows for different approval stages. This README.md file provides an overview of the module, including its features and instructions for installation and usage.

## Features

1. **Termination Workflow:** The module defines a multi-stage workflow for employee terminations, including stages like "Manager Approval," "IT Approval," "Finance Approval," and more.

2. **Kanban and Tree Views:** It offers Kanban and Tree views for visualizing the list of employee terminations and their current status.

3. **Automatic Sequence Generation:** The module automatically generates unique termination reference numbers (e.g., TER001, TER002) using the configured sequence.

4. **Security and Access Control:** Access to employee termination records is controlled based on user roles and groups, ensuring that only authorized personnel can perform actions at different stages of the termination process.

5. **Menu Items:** Menu items are provided to access different approval stages and terminated employee records directly from the Odoo user interface.

6. **Print Report:** It is possible to print the termination report with all dates and approvals

## Installation

To install and use the Odoo Employee Termination Module, follow these steps:

1. **Place Module Files:** Copy the Python files (`employee_termination.py`) into the appropriate directory in your Odoo installation, typically in the `model` folder.

2. **Add XML Files:** Copy the XML files into the `views` , `security` and `data` directories of your Odoo module.

3. **Update the Module List:** Go to the Odoo user interface and navigate to app. Search for your module and click "Install" to install the Employee Termination module.

## Usage

Once the Odoo Employee Termination Module is installed, you can follow these steps to use it:

1. **Creating Employee Terminations:**

   - Log in as an HR user or a user with relevant permissions.
   - Navigate to the "Termination" menu.
   - Click on the "Create" button to start a new termination request.
   - Fill in the required termination details.

2. **Processing Terminations:**

   - The termination request goes through various approval stages such as "Manager Approval," "IT Approval," "Finance Approval," and so on.
   - Users with appropriate group permissions can review and approve terminations at each stage.
   - Use the menu items for each approval stage to access and process terminations.

3. **Viewing Terminations:**

   - Use the Kanban and Tree views to visualize the list of employee terminations and their current status.
   - You can filter terminations by their state or use search functionality to find specific records.

4. **Generating Termination Sequences:**

   - The module automatically generates unique termination reference numbers based on the configured sequence.

5. **Access Control:**

   - Access to employee termination records is controlled based on user roles. Ensure that you have the necessary groups assigned to your users for the desired access.

## User Groups and Permissions

The Odoo Employee Termination Module defines several user groups for controlling access to different parts of the termination process. Here are some key user groups and their roles:

1. **ter_hrr_group:** HR Responsible Group
   - Members of this group have access to view and manage termination requests.
   - They can initiate the termination process and handle HR-related tasks.

2. **ter_it_group:** IT Group
   - Members of this group can approve terminations in the "IT Approval" stage.
   - They handle tasks related to IT resources.

3. **ter_finance_group:** Finance Group
   - Members of this group can approve terminations in the "Finance Approval" stage.
   - They handle financial aspects of terminations, such as salary and payslips.

4. **ter_law_group:** Legal Group
   - Members of this group can approve terminations in the "Legal Approval" stage.
   - They manage legal aspects of terminations, if applicable.

5. **ter_manager_group:** Manager Group
   - Members of this group can approve terminations in the "Manager Approval" stage.
   - They are typically the direct managers of the employees involved.

6. **ter_admin_group:** Administrator Group
   - Members of this group have full access to all parts of the module.
   - They can handle administration and configuration tasks.

## Code Structure

The Odoo Employee Termination Module code is organized as follows:

- **Python Files:**
  - `employee_termination.py`: Contains the core logic for managing employee terminations.

- **XML Files:**
  - `employee_termination_views.xml`: Defines the module's views, including Kanban, Tree, and Form views.
  - `security.xml`: Defines security groups and access record rules.
  - `termination_sequence.xml`: Configures the sequence for generating termination reference numbers.
  - `manager_approval.xml`: Configures menu items and views for different approval stages.

Customization:
You can customize and extend the Odoo Employee Termination Module to suit your organization's specific requirements. This may involve modifying the Python code and XML configurations to add additional fields, actions, or permissions.

License: This module is distributed under [License Name]. See [LICENSE.md] for more details.

Issues and Contributions:
If you encounter issues with this module or would like to contribute to its development, please report them on the [Issue Tracker](https://github.com/your-repo-link/issues).

---

