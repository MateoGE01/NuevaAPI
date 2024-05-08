import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Table from './Table';
import './App.css';

const App = () => {
    const [apiResponse, setApiResponse] = useState(null);
    const [apiResponseProcessed, setApiResponseProcessed] = useState(false);
    const [floors, setFloors] = useState([]);
    const cellNames = Array.from({ length: 10 }, (_, i) => String.fromCharCode(65 + i)).map(row => Array.from({ length: 21 }, (_, i) => `${row}${i + 1}`));
    const [occupiedMatrixes, setOccupiedMatrixes] = useState([]);
    const [typesList, setTypesList] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/sistema_parqueo/parqueadero/')
            .then(response => setApiResponse(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    useEffect (() => {
        if (apiResponse && !apiResponseProcessed) {
            console.log(apiResponse);
            // Processing
            const ubicationList = getParams(apiResponse, 'ubicacion');
            const floors = getFloors(ubicationList);
            setFloors(floors);
            const occupiedMatrixes= floors.map(floor => getOccupiedMatrix(floor));
            setOccupiedMatrixes(occupiedMatrixes);
            const types= getParams(apiResponse, 'tipo');
            const typesList = getTypesList(types);
            setTypesList(typesList);
            setApiResponseProcessed(true);
        }
    }
    , [apiResponse]);

    const getParams = (objectList, param) => {
        const list= objectList.map(object => object[param]);
        return list;
    }

    const getFloors = (ubicationList) => {
        const floors = ubicationList.map(ubicacion => ubicacion.slice(0, 2));
        const uniqueFloors = [...new Set(floors)];
        return uniqueFloors;
    }

    const getOccupiedMatrix = (floor) => {
        const occupiedMatrix = Array.from({ length: 10 }, () => Array.from({ length: 21 }, () => false));
        const floorUbications = apiResponse.filter(ubicacion => typeof ubicacion === 'string' && ubicacion.startsWith(floor));
        floorUbications.forEach(ubicacion => {
            const row = ubicacion.charCodeAt(2) - 65;
            const col = parseInt(ubicacion.slice(3)) - 1;
            occupiedMatrix[row][col] = true;
        });
        return occupiedMatrix;
    }

    const getTypesList = (types) => {
        const uniqueTypes = [...new Set(types)];
        return uniqueTypes;
    }

    return (
        <>
            <h1>App</h1>
            {floors.map((floor, index) => (
                <div key={index}>
                    <Table title={floor} cellNames={cellNames} occupiedMatrix={occupiedMatrixes[index]} listOfTypes={typesList} />
                </div>
            ))}
        </>
    );
}

export default App;
