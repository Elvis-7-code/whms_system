import {useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';
import PageLayout from '../../components/layout/PageLayout';
import Loader from '../../components/Loader';
import * as animalService from '../../services/animalService';

function AnimalDetail() {
  const { id } = useParams();
  const [animal, setAnimal] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    animalService
    .getAnimalById(id)
    .then(setAnimal)
    .catch(()=> setError('Could not load this animal.'))
    .finally(() => setIsLoading(false));
  }, [id]);

  return (<PageLayout>
    {isLoading && <Loader label="Loading animal details..." />}
    {error && <p className= 'form-error'> {error}</p>}
    {animal && (
      <div>
        <h1>{animal.name || animal.tagId}</h1>
        <p>species: {animal.species}</p>
        <p>breed: {animal.breed}</p>

        {/*TODO: breeding history, vacination records, feed logs tabs*/}
      </div>
    )}
  </PageLayout>);
}

export default AnimalDetail;