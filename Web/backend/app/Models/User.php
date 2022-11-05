<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    use HasFactory;

    protected $table = 'users';

    protected $fillable = [
        'id',
        'initials',
        'email',
        'phoneNumber',
        'group',
        'stateNumber',
        'access',
    ];

    protected $casts = [
        'created_at' => 'datetime',
    ];
}
