import { useNavigate } from "react-router-dom";
/**
 * Header Component
 * Renders a Bray header.
 */
const Header = () => {
    const navigate = useNavigate();

    const onClick = () => {
        navigate(`/sensors`);
    }

    return (
        <img className='logo' src='/bray_logo.png' alt='Bray Logo' onClick={onClick} />
    );
}

export default Header;
