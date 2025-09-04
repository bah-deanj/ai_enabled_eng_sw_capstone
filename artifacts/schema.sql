-- Table to store user information for all roles (New Hires, HR, Mentors, etc.)
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    user_role TEXT NOT NULL, -- e.g., 'Marketing Coordinator', 'Software Developer', 'HR Specialist'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table to store template onboarding tasks that can be assigned to users
CREATE TABLE onboarding_tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT -- e.g., 'HR', 'IT', 'Team-specific'
);

-- Junction table to assign specific tasks to users and track their progress
CREATE TABLE user_onboarding_checklists (
    checklist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'completed'
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES onboarding_tasks(task_id) ON DELETE CASCADE
);

-- Table to store various types of resources like documents, tutorials, and virtual tours
CREATE TABLE resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    resource_type TEXT NOT NULL, -- e.g., 'Documentation', 'Coding Standard', 'Tutorial', 'Virtual Tour', 'Training Module'
    content_url TEXT, -- Link to the actual content
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table to track user progress on resources like tutorials or training modules
CREATE TABLE user_resource_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started', -- e.g., 'not_started', 'in_progress', 'completed'
    completed_at DATETIME,
    last_accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE
);

-- Table to manage quizzes associated with training modules
CREATE TABLE quizzes (
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id INTEGER NOT NULL, -- Links the quiz to a specific 'Training Module' resource
    title TEXT NOT NULL,
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE
);

-- Table to store results of user attempts on quizzes
CREATE TABLE user_quiz_attempts (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score REAL,
    feedback TEXT,
    attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

-- Table to manage mentorship program connections
CREATE TABLE mentorships (
    mentorship_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_id INTEGER NOT NULL,
    mentee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'accepted', 'active', 'ended'
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    accepted_at DATETIME,
    FOREIGN KEY (mentor_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mentee_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table to manage social connections between users
CREATE TABLE social_connections (
    connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id INTEGER NOT NULL,
    addressee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', -- e.g., 'pending', 'accepted', 'rejected'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME,
    FOREIGN KEY (requester_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (addressee_id) REFERENCES users(user_id) ON DELETE CASCADE
);