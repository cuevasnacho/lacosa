import './CustomButton.css'

const CustomButton = ({label, onClick}) => {
    return (
        <button onClick={onClick}>
            {label}
        </button>
    );
};

export default CustomButton