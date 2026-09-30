import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { AppShell } from "./components/layout/AppShell";
import { LoginPage } from "./pages/LoginPage";
import { ActionsPage } from "./pages/ActionsPage";
import { InventoryPage } from "./pages/InventoryPage";
import { OcrPage } from "./pages/OcrPage";
import { ProfilePage } from "./pages/ProfilePage";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppShell />}>
            <Route path="/actions" element={<ActionsPage />} />
            <Route path="/inventory" element={<InventoryPage />} />
            <Route path="/ocr" element={<OcrPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/actions" replace />} />
      </Routes>
    </AuthProvider>
  );
}
