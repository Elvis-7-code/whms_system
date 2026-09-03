import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import PageLayout from '../../components/layout/PageLayout.jsx';
import Loader from '../../components/Loader.jsx';
import * as animalService from '../../services/animalService.js';

function AnimalsList() {
    const [animals, setAnimals] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        animalService
            .getAllAnimals()
            .then(setAnimals)
            .catch(() => setError('Could not load animals.'))
            .finally(() => setIsLoading(false));
    }, []);

return (
    <PageLayout>
        <h1>Animals List</h1>
        {isLoading && <Loader label="Loading animals..." />}
        {error && <p className="form-error">{error}</p>}
        {!isLoading && !error && (
            <ul className="animal-list">
                {animals.map((animal) => (
                    <li key={animal.id}>
                        <Link to={`/animals/${animal.id}`}>
                            {animal.name || animal.tagId}
                        </Link>
                    </li>
                ))}
                {animals.length === 0 && <p>No animals recorded yet.</p>}
            </ul>
        )};
        
    </PageLayout>
)};

export default AnimalsList;
