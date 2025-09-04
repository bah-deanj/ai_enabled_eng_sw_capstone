// day8_login_final.jsx
// Cleaned up design and text for onboarding dashboard

// Utility: MaterialIconWithLabel
const MaterialIconWithLabel = ({ icon, text }) => (
  <>
    <span className="material-icons align-middle">{icon}</span>
    <span className="mx-2 align-middle font-semibold">{text}</span>
  </>
);

// Sidebar navigation for PRD sections
const PRD_SECTIONS = [
  { label: "Onboarding", tooltip: "Onboarding Experience", icon: "assignment" },
  { label: "Progress", tooltip: "Progress Dashboard", icon: "trending_up" },
  { label: "Mentorship", tooltip: "Mentorship Program", icon: "group" },
  { label: "Social", tooltip: "Social Networking", icon: "people" },
];

const SidebarItem = ({ label, icon, active, onClick, tooltip }) => (
  <button
    className={`flex flex-col items-center w-16 py-2 rounded-lg transition group focus:outline-none ${active ? 'bg-blue-100 shadow border-blue-600 border' : 'hover:bg-gray-100'} mb-2`}
    onClick={onClick}
    title={tooltip}
    aria-label={label}
  >
    <span className={`material-icons ${active ? 'text-blue-600' : 'text-gray-400'} mb-1`} style={{ fontSize: '1.7rem' }}>{icon}</span>
    <span className={`text-xs font-medium ${active ? 'text-blue-700' : 'text-gray-500'}`}>{label}</span>
  </button>
);

const ProfileSidebar = ({ activeSection, setActiveSection }) => (
  <aside className="w-24 bg-white border-r p-4 flex flex-col items-center shadow-sm">
    <div className="bg-blue-500 p-3 rounded-full mb-6">
      <span className="material-icons text-white">account_circle</span>
    </div>
    <nav className="flex flex-col items-center mt-4">
      {PRD_SECTIONS.map((section, idx) => (
        <SidebarItem
          key={section.label}
          label={section.label}
          icon={section.icon}
          active={activeSection === idx}
          onClick={() => setActiveSection(idx)}
          tooltip={section.tooltip}
        />
      ))}
    </nav>
  </aside>
);

// WelcomeHeader Component
const WelcomeHeader = () => (
  <header className="flex items-center justify-between mb-8">
    <h1 className="text-3xl font-bold text-blue-900">Welcome, Sentient Shark!</h1>
    <div className="bg-white p-2 rounded-full shadow">
      <span className="material-icons text-blue-500">settings</span>
    </div>
  </header>
);

// OnboardingTaskItem Component
const OnboardingTaskItem = ({ text, checked = false, date, dateColor }) => {
  const id = `task-${text.replace(/\s+/g, '-').toLowerCase()}`;
  return (
    <li className="flex items-center py-1">
      <input type="checkbox" id={id} className="mr-2 accent-blue-500" checked={checked} readOnly />
      <label htmlFor={id} className="flex-1">{text}</label>
      {date && <span className={`ml-2 text-xs text-white ${dateColor} px-2 py-1 rounded`}>{date}</span>}
    </li>
  );
};

// TeamActionButton Component
const TeamActionButton = ({ text }) => (
  <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 mt-2 mr-2 transition">{text}</button>
);

// TeamMemberRow Component
const TeamMemberRow = ({ name, role, completion, completionColor }) => (
  <tr>
    <td className="py-2 font-medium">{name}</td>
    <td className="py-2 text-gray-600">{role}</td>
    <td className={`py-2 font-semibold ${completionColor || 'text-blue-600'}`}>{completion}</td>
  </tr>
);

// Carousel Dots Indicator
const CarouselDotsIndicator = ({ count, activeIndex }) => (
  <div className="flex space-x-2 mb-5 justify-center">
    {[...Array(count)].map((_, i) => (
      <span
        key={i}
        className={`rounded-full p-1 transition-all duration-200 ${i === activeIndex ? 'bg-blue-600 w-4 h-4' : 'bg-gray-300 w-3 h-3'}`}
      ></span>
    ))}
  </div>
);

// OnboardingJourneyHeader Component
const OnboardingJourneyHeader = () => (
  <div className="bg-blue-900 text-white px-6 py-3 rounded-full mb-6 flex items-center shadow">
    <MaterialIconWithLabel icon="account_circle" text="Onboarding Journey" />
    <span className="material-icons ml-4">camera_alt</span>
  </div>
);

// OnboardingChecklistCard Component
const OnboardingChecklistCard = () => (
  <section className="bg-white rounded-lg shadow-md p-6 w-80">
    <h2 className="font-bold text-lg mb-3 text-blue-900">Onboarding Checklist</h2>
    <div className="mb-4">
      <span className="block text-sm text-gray-600 mb-1">Progress</span>
      <div className="relative pt-1">
        <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-blue-200">
          <div style={{ width: '60%' }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-blue-600"></div>
        </div>
      </div>
    </div>
    <button className="text-blue-600 underline mb-4">Customize Checklist</button>
    <div className="mb-4">
      <h3 className="font-semibold mb-2">Tasks</h3>
      <ul className="text-sm list-disc list-inside">
        <OnboardingTaskItem text="Complete Profile" />
        <OnboardingTaskItem text="Upload Documents" />
        <OnboardingTaskItem text="Review Policies" />
      </ul>
    </div>
    <div className="text-gray-500 text-sm">
      <p>Tip: You can update your progress anytime.</p>
    </div>
  </section>
);

// ResourceLibraryCard Component
const ResourceLibraryCard = () => (
  <section className="bg-white rounded-lg shadow-md p-6 w-80">
    <h2 className="font-bold text-lg mb-3 text-blue-900">Resources</h2>
    <div className="mb-4 bg-orange-100 p-3 rounded flex flex-col items-center">
      <span className="material-icons mb-2 text-orange-500" style={{ fontSize: '2rem' }}>library_books</span>
      <p className="mb-2 text-gray-700">Access the Resource Library</p>
      <button className="bg-orange-500 hover:bg-orange-600 text-white rounded-lg px-4 py-2 mt-2 transition">Explore</button>
    </div>
    <div className="mb-4">
      <p className="text-gray-700">Find guides, FAQs, and more.</p>
      <button className="bg-orange-500 hover:bg-orange-600 text-white rounded-lg px-4 py-2 mt-2 transition">Learn More</button>
    </div>
  </section>
);

// InteractiveTutorialsCard Component
const InteractiveTutorialsCard = () => (
  <section className="bg-white rounded-lg shadow-md p-6 w-80">
    <h2 className="font-bold text-lg mb-3 text-blue-900">Interactive Tutorials</h2>
    <div className="mb-4 bg-orange-100 p-3 rounded flex flex-col items-center">
      <span className="material-icons mb-2 text-orange-500" style={{ fontSize: '2rem' }}>school</span>
      <p className="mb-2 text-gray-700">Step-by-step onboarding help</p>
      <button className="bg-orange-500 hover:bg-orange-600 text-white rounded-lg px-4 py-2 mt-2 transition">Start Tutorial</button>
    </div>
  </section>
);

// OnboardingOverviewCard Component
const OnboardingOverviewCard = () => (
  <section className="bg-white p-6 rounded-lg shadow-md w-1/2">
    <h2 className="text-lg font-bold mb-4 text-blue-900">My Onboarding Overview</h2>
    <div className="flex items-center mb-4">
      <div className="w-16 h-16 border-4 border-blue-600 rounded-full flex items-center justify-center">
        <span className="text-xl font-bold text-blue-600">60%</span>
      </div>
    </div>
    <div>
      <h3 className="font-semibold mb-2">Today's Tasks</h3>
      <ul className="space-y-2">
        <OnboardingTaskItem text="Complete Benefits Enrollment" />
        <OnboardingTaskItem text="Review Employee Handbook" checked date="Jul 26" dateColor="bg-yellow-500" />
        <OnboardingTaskItem text="Set Up Workstation" date="Jul 26" dateColor="bg-gray-300" />
      </ul>
    </div>
  </section>
);

// TeamDashboardCard Component
const TeamDashboardCard = () => (
  <section className="bg-white p-6 rounded-lg shadow-md w-1/2">
    <h2 className="text-lg font-bold mb-4 text-blue-900">Team & HR Dashboard</h2>
    <table className="w-full mb-4">
      <thead>
        <tr>
          <th className="text-left font-semibold">Name</th>
          <th className="text-left font-semibold">Role</th>
          <th className="text-left font-semibold">Completion</th>
        </tr>
      </thead>
      <tbody>
        <TeamMemberRow name="Jane Cooper" role="Marketing Coordinator" completion="75%" />
        <TeamMemberRow name="Ronald Richards" role="Sales Associate" completion="Overdue" completionColor="text-red-600" />
        <TeamMemberRow name="Cody Fisher" role="Product Designer" completion="60%" />
      </tbody>
    </table>
    <div className="flex flex-wrap gap-2">
      <TeamActionButton text="Assign Role-Specific Task" />
      <TeamActionButton text="Send Reminder" />
      <TeamActionButton text="Collect Feedback" />
    </div>
  </section>
);

// Carousel-style OnboardingCardsPanel
const OnboardingCardsPanel = () => {
  const cards = [
    <OnboardingChecklistCard key="checklist" />,
    <ResourceLibraryCard key="resources" />,
    <InteractiveTutorialsCard key="tutorials" />,
  ];
  const [activeIndex, setActiveIndex] = React.useState(0);

  const goPrev = () => setActiveIndex(i => (i === 0 ? cards.length - 1 : i - 1));
  const goNext = () => setActiveIndex(i => (i === cards.length - 1 ? 0 : i + 1));

  return (
    <div className="flex flex-col items-center w-full">
      <OnboardingJourneyHeader />
      <CarouselDotsIndicator count={cards.length} activeIndex={activeIndex} />
      <div className="flex items-center justify-center w-full" style={{ minHeight: '370px' }}>
        <button
          className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center shadow hover:bg-blue-700 mx-4 text-3xl border-2 border-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          onClick={goPrev}
          aria-label="Previous"
        >
          {/* Use Unicode left chevron if Material Icons font is not loaded */}
          <span style={{ fontSize: '2rem', lineHeight: 1 }}>&#x25C0;</span>
        </button>
        <div className="transition-all duration-300 w-80">
          {cards[activeIndex]}
        </div>
        <button
          className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center shadow hover:bg-blue-700 mx-4 text-3xl border-2 border-white focus:outline-none focus:ring-2 focus:ring-blue-400"
          onClick={goNext}
          aria-label="Next"
        >
          {/* Use Unicode right chevron if Material Icons font is not loaded */}
          <span style={{ fontSize: '2rem', lineHeight: 1 }}>&#x25B6;</span>
        </button>
      </div>
    </div>
  );
};

// MainDashboardLayout with PRD section navigation
const MainDashboardLayout = () => {
  const [activeSection, setActiveSection] = React.useState(0);

  let mainContent;
  switch (activeSection) {
    case 0:
      mainContent = <OnboardingCardsPanel />;
      break;
    case 1:
      mainContent = <OnboardingOverviewCard />;
      break;
    case 2:
      mainContent = (
        <section className="bg-white rounded-lg shadow-md p-6 w-80">
          <h2 className="font-bold text-lg mb-3 text-blue-900">Mentorship Program</h2>
          <p className="mb-2 text-gray-700">Connect with experienced mentors based on your role and interests.</p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 mt-2 transition">Find a Mentor</button>
        </section>
      );
      break;
    case 3:
      mainContent = (
        <section className="bg-white rounded-lg shadow-md p-6 w-80">
          <h2 className="font-bold text-lg mb-3 text-blue-900">Social Networking</h2>
          <p className="mb-2 text-gray-700">Connect with peers and other employees.</p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 mt-2 transition">Network Now</button>
        </section>
      );
      break;
    default:
      mainContent = <OnboardingCardsPanel />;
  }

  return (
    <div className="flex min-h-screen bg-blue-100">
      <ProfileSidebar activeSection={activeSection} setActiveSection={setActiveSection} />
      <div className="flex-1 flex flex-col p-8">
        <WelcomeHeader />
        <div className="flex justify-center items-start">
          {mainContent}
        </div>
      </div>
    </div>
  );
};


// LoginScreen Component
const LoginScreen = ({ onLogin }) => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState("");
  const [showCreateUser, setShowCreateUser] = React.useState(false);
  const [newEmail, setNewEmail] = React.useState("");
  const [newPassword, setNewPassword] = React.useState("");
  const [showModal, setShowModal] = React.useState(false);
  const [modalMsg, setModalMsg] = React.useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simple check (replace with real auth in production)
    if (email === "asharkwhois@sentient.gov" && password === "password") {
      onLogin();
    } else {
      setError("Invalid credentials. Try asharkwhois@sentient.gov / password.");
    }
  };

  const handleCreateUser = (e) => {
    e.preventDefault();
    // Fake success/failure
    if (newEmail && newPassword) {
      setModalMsg("User created successfully!");
    } else {
      setModalMsg("Failed to create user. Please fill out all fields.");
    }
    setShowModal(true);
  };

  const handleReturnToLogin = () => {
    setShowModal(false);
    setShowCreateUser(false);
    setNewEmail("");
    setNewPassword("");
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-blue-100">
      {!showCreateUser ? (
        <form className="bg-white p-8 rounded-lg shadow-md w-96" onSubmit={handleSubmit}>
          <h2 className="text-2xl font-bold mb-6 text-blue-900 text-center">Login</h2>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Email</label>
            <input type="email" className="w-full p-2 border rounded" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Password</label>
            <input type="password" className="w-full p-2 border rounded" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          {error && <div className="text-red-500 mb-4">{error}</div>}
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 w-full font-semibold">Login</button>
          <button type="button" className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 w-full font-semibold mt-4" onClick={() => setShowCreateUser(true)}>Create User</button>
        </form>
      ) : (
        <form className="bg-white p-8 rounded-lg shadow-md w-96" onSubmit={handleCreateUser}>
          <h2 className="text-2xl font-bold mb-6 text-blue-900 text-center">Create User</h2>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Email</label>
            <input type="email" className="w-full p-2 border rounded" value={newEmail} onChange={e => setNewEmail(e.target.value)} />
          </div>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Password</label>
            <input type="password" className="w-full p-2 border rounded" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          </div>
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 w-full font-semibold">SUBMIT</button>
        </form>
      )}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white p-6 rounded-lg shadow-md w-80 flex flex-col items-center">
            <span className="text-lg font-semibold mb-4">{modalMsg}</span>
            <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 w-full font-semibold mt-2" onClick={handleReturnToLogin}>Return to Login</button>
          </div>
        </div>
      )}
    </div>
  );
}

// App Component to handle login state
const App = () => {
  const [loggedIn, setLoggedIn] = React.useState(false);
  return loggedIn ? <MainDashboardLayout /> : <LoginScreen onLogin={() => setLoggedIn(true)} />;
};

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<App />);
