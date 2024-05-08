import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import'./Table.css';

const Table = ({ title, cellNames, occupiedMatrix, listOfTypes }) => {
    const isOccupied = (row, col) => {
        return occupiedMatrix[row][col];
    };

    const setIsOccupied = (row, col, value) => {
        occupiedMatrix[row][col] = value;
    };

    const routeForCell = (title, row, col) =>{
        // Stick the title to the cell name and return it
        const cellName = cellNames[row][col];
        return `${title}${cellName}`;
    };
    

    return (
        <table>
            <caption>{title}</caption>
            <tbody>
                {cellNames.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                        {row.map((cell, cellIndex) => (
                            <td key={cellIndex} className={occupiedMatrix[rowIndex][cellIndex]? 'Ocupado':'Desocupado'}>{cell}</td>
                        ))}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default Table;