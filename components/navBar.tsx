import Link from "next/link";
import React from 'react';

const NavBar: React.FC = () => {
    return (
        <nav style={styles.nav} className=" flex items-center justify-center">
            <Link href="/" className="font-bold border border-black rounded-full p-3">
                Home
            </Link>
        </nav>
    );
};

const styles = {
    nav: {
        display: 'flex',
        padding: '10px',
    },
    button: {
        color: '#fff',
        backgroundColor: '#0070f3',
        border: 'none',
        padding: '10px 20px',
        cursor: 'pointer',
        borderRadius: '5px',
    },
};

export default NavBar;