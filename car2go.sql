CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nom CHARACTER VARYING(100) NOT NULL,
    prenom CHARACTER VARYING(100) NOT NULL,
    email CHARACTER VARYING(100) UNIQUE NOT NULL,
    password CHARACTER VARYING(255) NOT NULL,
    telephone CHARACTER VARYING(15) NOT NULL,
    adresse CHARACTER VARYING(255) NOT NULL,
    date_naissance DATE NOT NULL,
    role CHARACTER VARYING(20) NOT NULL CHECK (role IN ('apprenti', 'accompagnateur')),
    license_date DATE,
    numero_permis CHARACTER VARYING(20) UNIQUE CHECK (role = 'accompagnateur' AND numero_permis IS NOT NULL),
    numero_livret CHARACTER VARYING(20) UNIQUE CHECK (role = 'apprenti' AND numero_livret IS NOT NULL),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    nom CHARACTER VARYING(100) NOT NULL,
    modele CHARACTER VARYING(100) NOT NULL,
    annee_fab INTEGER NOT NULL,
    type CHARACTER VARYING(20) NOT NULL CHECK (type IN ('double commande', 'classique')),
    plaque CHARACTER VARYING(20) UNIQUE NOT NULL,
    controle_technique DATE NOT NULL,
    prix_par_heure DECIMAL(10,2) NOT NULL DEFAULT 20.00,
    disponible BOOLEAN DEFAULT TRUE,
    image_url CHARACTER VARYING(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    car_id INTEGER REFERENCES cars(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT NOW(),
    status CHARACTER VARYING(20) DEFAULT 'pending',
    purpose CHARACTER VARYING(20) NOT NULL CHECK (purpose IN ('self', 'accompanied')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);