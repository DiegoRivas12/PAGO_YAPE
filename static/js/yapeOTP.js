async function initializeMP() {
    try {
        const response = await fetch("/get_public_key");
        const data = await response.json();
        const mp = new MercadoPago(data.public_key);  // Se obtiene la clave pública desde el backend
        
        window.mpInstance = mp; // Guardar la instancia para reutilizar
    } catch (error) {
        console.error("Error obteniendo la clave pública:", error);
    }
}

async function handleYape() {
    const phoneNumber = document.getElementById("form-checkout__payerPhone").value;
    const otp = document.getElementById("form-checkout__payerOTP").value;

    if (!window.mpInstance) {
        console.error("MercadoPago no ha sido inicializado.");
        return;
    }

    try {
        const yape = window.mpInstance.yape({ otp, phoneNumber });
        const yapeToken = await yape.create();

        console.log("Token generado:", yapeToken);

        // Enviar el token al backend para procesar el pago
        const response = await fetch("/procesar_pago", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token: yapeToken, phoneNumber })
        });

        const result = await response.json();
        console.log("Respuesta del pago:", result);
    } catch (error) {
        console.error("Error generando el token:", error);
    }
}

initializeMP();  // Inicializar MercadoPago al cargar la página