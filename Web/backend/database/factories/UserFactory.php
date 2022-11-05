<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<User>
 */
class UserFactory extends Factory
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
            'access' => 'S',
        ];
    }
    public function default(): array
    {
        return [
            'id' => 1,
            'initials' => fake()->firstName() . ' ' . fake()->lastName(),
            'email' => fake()->email(),
            'phoneNumber' => fake()->phoneNumber(),
            'group' => '24' . rand(100, 410),
            'stateNumber' => 'A' . rand(100,999) . 'AA|'. rand(1,999),
            'access' => 'S',
        ];
    }
}
