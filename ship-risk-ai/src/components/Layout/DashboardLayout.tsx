import React from 'react';
import { Outlet } from 'react-router-dom';
import { Header } from '../Common/Header';
import { Sidebar } from '../Common/Sidebar';
import { Footer } from '../Common/Footer';

export const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 overflow-auto">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  );
};
