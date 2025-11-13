import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import MainLayout from '../layouts/MainLayout';

const ProtectedRoute = () => {
    const { user, loading } = useUser();

    if (loading) {
        // You can add a spinner or a loading screen here
        return <div>Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/login" />;
    }

    return (
        <MainLayout>
            <Outlet />
        </MainLayout>
    );
};

export default ProtectedRoute;
