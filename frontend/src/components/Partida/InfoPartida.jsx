import Partida from './Partida.jsx';

const Home = function () {
  const user_id = JSON.parse(localStorage.getItem('user_id'));
  const ws = new WebSocket(`ws://localhost:8000/ws/${user_id}`);

  return (
    <Partida ws={ws} />
  );
};

export default Home;