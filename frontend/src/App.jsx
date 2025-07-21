import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Layout } from "./layout/Layout.jsx";
import { ChallengeGenerator } from "./challenge/ChallengeGenerator.jsx";
import { HistoryPannel } from "./history/HistoryPanel.jsx";
import { AuthenticationPage } from "./auth/AuthenticationPage.jsx";
import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.jsx";

function App() {
  return (
    <ClerkProviderWithRoutes>
      <Routes>
        <Route path="/sign-in/*" element={<AuthenticationPage />} />
        <Route path="/sign-up/" element={<AuthenticationPage />} />

        <Route element={<Layout />}>
          <Route path="/" element={<ChallengeGenerator />} />
          <Route path="/history" element={<HistoryPannel />} />
        </Route>
      </Routes>
    </ClerkProviderWithRoutes>
  );
}

export default App;

/* 

Purpose: Styling, Routing, Authentication Wrapper

- App.css contains all general styling for this react app
- React Route library is used to set up app routes

- Route paths are customizable. 
- /* allows clerk to use nested routes; ex: sign-in/verify-email

- The <Route element {<Layout/>} defines a Layout wrapper 
- Any routes inside will be rendered inside the Layout Component
- The Layout Route defines a common structures of the pages.

*/