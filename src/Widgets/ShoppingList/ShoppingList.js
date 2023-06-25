export default function ShoppingList() {

    useEffect( () => {

        const fetchData = async () => {
            const response = await axios("api/alexa");
            setWeatherData(response.data)
          };
      
          const interval = setInterval(() => {
            fetchData();
          }, 1000 * 60 * 24); // Refreshes the weather
          fetchData();

    }, [])




}