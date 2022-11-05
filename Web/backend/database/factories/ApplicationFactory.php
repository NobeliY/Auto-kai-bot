<?php

namespace Database\Factories;

use App\Models\Application;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Application>
 */
class ApplicationFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'id' => rand(1, 9999999),
            'initials' => fake()->firstName() . ' ' . fake()->lastName(),
            'email' => fake()->email(),
            'phoneNumber' => fake()->phoneNumber(),
            'group' => '24' . rand(100, 410),
            'stateNumber' => 'A' . rand(100,999) . 'AA|'. rand(1,999),
        ];
    }
}
