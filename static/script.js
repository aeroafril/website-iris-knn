function parseDecimal(value){
    const cleaned = value.trim().replace(',', '.');
    if(!/^-?\d+(\.\d+)?$/.test(cleaned)) return NaN;
    return parseFloat(cleaned);
}

document.querySelector('form').addEventListener('submit', async(e) => {
    e.preventDefault();

    const ids = ['SL', 'SW', 'PL', 'PW'];
    const features = ids.map(id => parseDecimal(document.getElementById(id).value));

    if(features.some(Number.isNaN)){
        alert('Semua input harus berupa angka yang valid (contoh: 1,4 atau 1.4)');
        return;
    }

    const hasil = document.getElementById('hasil');

    try{
        hasil.textContent = 'Menghitung prediksi...';
        hasil.style.color = 'black';

        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sepal_length: features[0],
                sepal_weight: features[1],
                petal_length: features[2],
                petal_weight: features[3]
            })
        });

        if(!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        hasil.innerText = "Hasil Prediksi: " + data.prediction;
    }catch(error){
        console.error('Terjadi kesalahan: ', error);
        hasil.textContent = 'Gagal terhubung ke server'
    }
});